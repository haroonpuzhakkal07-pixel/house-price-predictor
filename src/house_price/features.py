import pandas as pd


def create_features(df):
    """
    Apply the feature engineering used during model training.
    """

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
    df["HouseAge"] = df["YrSold"] - df["YearBuilt"]

    df["RemodAge"] = (
        df["YrSold"] - df["YearRemodAdd"]
    ).clip(lower=0)

    df["GarageAge"] = (
        df["YrSold"] - df["GarageYrBlt"]
    )

    df["GarageAge"] = df["GarageAge"].where(
        df["GarageYrBlt"] > 0,
        0
    )

    # Quality × size features
    df["Qual_GrLivArea"] = (
        df["OverallQual"] * df["GrLivArea"]
    )

    df["Qual_TotalSF"] = (
        df["OverallQual"] * df["TotalSF"]
    )

    df["Qual_TotalBsmtSF"] = (
        df["OverallQual"] * df["TotalBsmtSF"]
    )

    # Additional domain features
    df["TotalLivingArea"] = (
        df["GrLivArea"] + df["TotalBsmtFinishedSF"]
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