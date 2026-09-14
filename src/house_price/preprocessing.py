import pandas as pd


ABSENCE_CATEGORICAL_COLS = [
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

ABSENCE_NUMERICAL_COLS = [
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


def preprocess_data(df, training_df=None):
    """
    Apply the preprocessing used during model development.

    Parameters
    ----------
    df : pd.DataFrame
        Data to preprocess.

    training_df : pd.DataFrame, optional
        Training data used for training-derived imputations such as
        categorical modes.
    """

    df = df.copy()

    # Structural categorical missing values
    for col in ABSENCE_CATEGORICAL_COLS:
        df[col] = df[col].fillna("NoFeature")

    # Structural numerical missing values
    for col in ABSENCE_NUMERICAL_COLS:
        df[col] = df[col].fillna(0)

    # LotFrontage: neighborhood median
    df["LotFrontage"] = df.groupby(
        "Neighborhood"
    )["LotFrontage"].transform(
        lambda x: x.fillna(x.median())
    )

    # Electrical
    if training_df is not None:
        electrical_mode = training_df["Electrical"].mode()[0]
        df["Electrical"] = df["Electrical"].fillna(
            electrical_mode
        )

    # Masonry veneer area
    df["MasVnrArea"] = df["MasVnrArea"].fillna(0)

    # Masonry veneer type
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

    # Known data-quality correction
    df.loc[
        df["GarageYrBlt"] > df["YrSold"],
        "GarageYrBlt"
    ] = df["YearBuilt"] + 1

    # Remaining categorical missing values
    if training_df is not None:
        categorical_cols = [
            "MSZoning",
            "Utilities",
            "Functional",
            "Exterior1st",
            "Exterior2nd",
            "KitchenQual",
            "SaleType",
        ]

        for col in categorical_cols:
            mode = training_df[col].mode()[0]
            df[col] = df[col].fillna(mode)

    return df