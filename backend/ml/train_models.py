import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

from preprocess import load_and_preprocess


def train_models(csv_path):

    # Load processed data
    X, y = load_and_preprocess(csv_path)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {}

    for target in y.columns:
        model = LinearRegression()
        model.fit(X_train, y_train[target])

        models[target] = model

        # Save model
        joblib.dump(model, f"backend/ml/{target}_model.pkl")

    print("Training complete. Models saved.")


if __name__ == "__main__":
    train_models("data/survey_data.csv")