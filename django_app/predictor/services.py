import json
from pathlib import Path

from src.house_price.predict import predict_price


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HOUSE_PATH = PROJECT_ROOT / "artifacts" / "default_house.json"


# Load once when Django starts.
with open(DEFAULT_HOUSE_PATH, "r", encoding="utf-8") as file:
    DEFAULT_HOUSE = json.load(file)


def build_prediction_input(form_data):
    """
    Build a complete model input from the user-facing form.

    Default values come from a representative training-data row.
    User-provided values override those defaults.
    """

    data = DEFAULT_HOUSE.copy()

    data.update(
        {
            "OverallQual": form_data["overall_qual"],
            "OverallCond": form_data["overall_cond"],
            "Neighborhood": form_data["neighborhood"],
            "GrLivArea": form_data["gr_liv_area"],
            "TotalBsmtSF": form_data["total_bsmt_sf"],
            "1stFlrSF": form_data["first_flr_sf"],
            "2ndFlrSF": form_data["second_flr_sf"],
            "LotArea": form_data["lot_area"],
            "YearBuilt": form_data["year_built"],
            "YearRemodAdd": form_data["year_remod_add"],
            "FullBath": form_data["full_bath"],
            "HalfBath": form_data["half_bath"],
            "BedroomAbvGr": form_data["bedroom_abv_gr"],
            "TotRmsAbvGrd": form_data["tot_rms_abv_grd"],
            "ExterQual": form_data["exter_qual"],
            "KitchenQual": form_data["kitchen_qual"],
            "GarageCars": form_data["garage_cars"],
            "GarageArea": form_data["garage_area"],
            "GarageYrBlt": form_data["garage_yr_blt"],
            "GarageFinish": form_data["garage_finish"],
            "BsmtQual": form_data["bsmt_qual"],
            "YrSold": form_data["year_sold"],
            "MoSold": form_data["month_sold"],
        }
    )

    return data


def predict_from_form(form):
    """Generate a house-price prediction from a validated Django form."""

    property_data = build_prediction_input(form.cleaned_data)

    return predict_price(property_data)