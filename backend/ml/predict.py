import joblib
import pandas as pd


# Load trained models
models = {
    "electricity": joblib.load("backend/ml/willing_electricity_reduction_model.pkl"),
    "transport": joblib.load("backend/ml/willing_transport_shift_model.pkl"),
    "diet": joblib.load("backend/ml/willing_diet_reduction_model.pkl"),
    "waste": joblib.load("backend/ml/willing_waste_reduction_model.pkl")
}


def predict_adoption_probabilities(user_input_df):
    """
    user_input_df: preprocessed dataframe with same columns as training features
    """

    predictions = {}

    for action, model in models.items():
        score = model.predict(user_input_df)[0]

        # normalize 1–5 score to probability
        probability = score / 5.0

        # clamp values between 0 and 1
        probability = max(0, min(1, probability))

        predictions[action] = probability

    return predictions