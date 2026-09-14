import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline

from catboost import CatBoostRegressor


class HousePriceModel(BaseEstimator, RegressorMixin):

    RANDOM_STATE = 42

    ordinal_mappings = {
        "ExterQual": ["Po", "Fa", "TA", "Gd", "Ex"],
        "ExterCond": ["Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtQual": ["NoFeature", "Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtCond": ["NoFeature", "Po", "Fa", "TA", "Gd", "Ex"],
        "BsmtExposure": ["NoFeature", "No", "Mn", "Av", "Gd"],
        "BsmtFinType1": [
            "NoFeature", "Unf", "LwQ", "Rec",
            "BLQ", "ALQ", "GLQ"
        ],
        "BsmtFinType2": [
            "NoFeature", "Unf", "LwQ", "Rec",
            "BLQ", "ALQ", "GLQ"
        ],
        "HeatingQC": ["Po", "Fa", "TA", "Gd", "Ex"],
        "KitchenQual": ["Po", "Fa", "TA", "Gd", "Ex"],
        "FireplaceQu": ["NoFeature", "Po", "Fa", "TA", "Gd", "Ex"],
        "GarageFinish": ["NoFeature", "Unf", "RFn", "Fin"],
        "GarageQual": ["NoFeature", "Po", "Fa", "TA", "Gd", "Ex"],
        "GarageCond": ["NoFeature", "Po", "Fa", "TA", "Gd", "Ex"],
        "PavedDrive": ["N", "P", "Y"],
        "Functional": [
            "Sev", "Maj2", "Maj1", "Mod",
            "Min2", "Min1", "Typ"
        ],
        "PoolQC": ["NoFeature", "Fa", "Gd", "Ex"],
        "Fence": ["NoFeature", "MnWw", "GdWo", "MnPrv", "GdPrv"],
    }

    absence_cols = [
        "PoolQC",
        "MiscFeature",
        "Alley",
        "Fence",
        "FireplaceQu",
        "GarageType",
        "GarageFinish",
        "GarageQual",
        "GarageCond",
        "BsmtQual",
        "BsmtCond",
        "BsmtExposure",
        "BsmtFinType1",
        "BsmtFinType2",
    ]

    absence_num_cols = [
        "GarageYrBlt",
        "GarageCars",
        "GarageArea",
        "BsmtFinSF1",
        "BsmtFinSF2",
        "BsmtUnfSF",
        "TotalBsmtSF",
        "BsmtFullBath",
        "BsmtHalfBath",
    ]

    remaining_categorical_cols = [
        "MSZoning",
        "Utilities",
        "Functional",
        "Exterior1st",
        "Exterior2nd",
        "KitchenQual",
        "SaleType",
    ]

    def __init__(self):
        self.model = None
        self.neighborhood_medians = None
        self.electrical_mode = None
        self.categorical_modes = None

    def _preprocess(self, df):

        df = df.copy()

        # Structural categorical missing values
        for col in self.absence_cols:
            df[col] = df[col].fillna("NoFeature")

        # Structural numerical missing values
        for col in self.absence_num_cols:
            df[col] = df[col].fillna(0)

        # LotFrontage using training neighborhood medians
        df["LotFrontage"] = df["LotFrontage"].fillna(
            df["Neighborhood"].map(self.neighborhood_medians)
        )

        # Fallback to global training median
        df["LotFrontage"] = df["LotFrontage"].fillna(
            self.global_lotfrontage_median
        )

        # Electrical
        df["Electrical"] = df["Electrical"].fillna(
            self.electrical_mode
        )

        # Masonry veneer
        df["MasVnrArea"] = df["MasVnrArea"].fillna(0)

        df.loc[
            df["MasVnrType"].isna()
            & (df["MasVnrArea"] == 0),
            "MasVnrType"
        ] = "NoFeature"

        df.loc[
            df["MasVnrType"].isna()
            & (df["MasVnrArea"] > 0),
            "MasVnrType"
        ] = "Unknown"

        # Suspicious value identified during audit
        df.loc[
            df["GarageYrBlt"] > df["YrSold"],
            "GarageYrBlt"
        ] = df["YearBuilt"] + 1

        # Remaining categorical values
        for col in self.remaining_categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna(
                    self.categorical_modes[col]
                )

        return df

    def _create_features(self, df):

        df = df.copy()

        # Area features
        df["TotalSF"] = (
            df["TotalBsmtSF"]
            + df["1stFlrSF"]
            + df["2ndFlrSF"]
        )

        df["TotalBathrooms"] = (
            df["FullBath"]
            + 0.5 * df["HalfBath"]
            + df["BsmtFullBath"]
            + 0.5 * df["BsmtHalfBath"]
        )

        df["TotalPorchSF"] = (
            df["OpenPorchSF"]
            + df["3SsnPorch"]
            + df["EnclosedPorch"]
            + df["ScreenPorch"]
            + df["WoodDeckSF"]
        )

        df["TotalBsmtFinishedSF"] = (
            df["BsmtFinSF1"]
            + df["BsmtFinSF2"]
        )

        # Age features
        df["HouseAge"] = (
            df["YrSold"] - df["YearBuilt"]
        )

        df["RemodAge"] = (
            df["YrSold"] - df["YearRemodAdd"]
        )

        df["GarageAge"] = (
            df["YrSold"] - df["GarageYrBlt"]
        )

        df["GarageAge"] = df["GarageAge"].where(
            df["GarageYrBlt"] > 0,
            0
        )

        # Quality × size
        df["Qual_GrLivArea"] = (
            df["OverallQual"] * df["GrLivArea"]
        )

        df["Qual_TotalSF"] = (
            df["OverallQual"] * df["TotalSF"]
        )

        df["Qual_TotalBsmtSF"] = (
            df["OverallQual"] * df["TotalBsmtSF"]
        )

        # Additional features
        df["TotalLivingArea"] = (
            df["GrLivArea"]
            + df["TotalBsmtFinishedSF"]
        )

        df["TotalRooms"] = (
            df["TotRmsAbvGrd"]
            + df["FullBath"]
            + df["HalfBath"]
        )

        df["AreaPerRoom"] = (
            df["GrLivArea"]
            / df["TotRmsAbvGrd"].clip(lower=1)
        )

        df["GarageAreaPerCar"] = (
            df["GarageArea"]
            / df["GarageCars"].clip(lower=1)
        )

        return df

    def _build_model(self, X):

        ordinal_cols = list(self.ordinal_mappings.keys())

        categorical_cols = X.select_dtypes(
            include=["object", "str"]
        ).columns.tolist()

        nominal_cols = [
            col
            for col in categorical_cols
            if col not in ordinal_cols
        ]

        categorical_cols_to_onehot = nominal_cols + [
            "MSSubClass",
            "MoSold",
            "YrSold",
        ]

        ordinal_categories = [
            self.ordinal_mappings[col]
            for col in ordinal_cols
        ]

        tree_preprocessor = ColumnTransformer(
            transformers=[
                (
                    "ord",
                    OrdinalEncoder(
                        categories=ordinal_categories,
                        handle_unknown="use_encoded_value",
                        unknown_value=-1,
                    ),
                    ordinal_cols,
                ),
                (
                    "nom",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False,
                    ),
                    categorical_cols_to_onehot,
                ),
            ],
            remainder="passthrough",
        )

        return Pipeline([
            (
                "preprocessor",
                tree_preprocessor
            ),
            (
                "model",
                CatBoostRegressor(
                    iterations=800,
                    learning_rate=0.05,
                    depth=7,
                    l2_leaf_reg=5,
                    loss_function="RMSE",
                    random_seed=self.RANDOM_STATE,
                    verbose=False,
                    thread_count=-1,
                ),
            ),
        ])

    def fit(self, X, y):

        X = X.copy()
        y = np.asarray(y)

        # Store training-derived imputation values
        self.neighborhood_medians = (
            X.groupby("Neighborhood")["LotFrontage"]
            .median()
            .to_dict()
        )

        self.global_lotfrontage_median = (
            X["LotFrontage"].median()
        )

        self.electrical_mode = (
            X["Electrical"].mode()[0]
        )

        self.categorical_modes = {
            col: X[col].mode()[0]
            for col in self.remaining_categorical_cols
            if col in X.columns
        }

        # Preprocessing
        X = self._preprocess(X)

        # Feature engineering
        X = self._create_features(X)

        # Remove target if accidentally supplied
        if "SalePrice" in X.columns:
            X = X.drop(columns=["SalePrice"])

        # Remove identifier
        if "Id" in X.columns:
            X = X.drop(columns=["Id"])

        # Build and train model
        self.model = self._build_model(X)

        self.model.fit(X, y)

        return self

    def predict(self, X):

        if self.model is None:
            raise RuntimeError(
                "Model has not been fitted."
            )

        X = self._preprocess(X)
        X = self._create_features(X)

        if "SalePrice" in X.columns:
            X = X.drop(columns=["SalePrice"])

        if "Id" in X.columns:
            X = X.drop(columns=["Id"])

        # Model predicts log1p(SalePrice)
        log_prediction = self.model.predict(X)

        # Convert back to original price scale
        prediction = np.expm1(log_prediction)

        # Ensure non-negative prices
        return np.maximum(prediction, 0)