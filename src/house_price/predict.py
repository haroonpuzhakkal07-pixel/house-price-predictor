import sys
from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "house_price_model.joblib"
)


# Load the model once when the service starts
model = joblib.load(MODEL_PATH)


def predict_price(property_data):
    """
    Predict the SalePrice for a single property.

    Parameters
    ----------
    property_data : dict
        Raw property features.

    Returns
    -------
    float
        Predicted SalePrice.
    """

    # Convert input dictionary to a one-row DataFrame
    input_data = pd.DataFrame([property_data])

    # Generate prediction
    prediction = model.predict(input_data)[0]

    return float(prediction)