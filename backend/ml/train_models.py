import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from preprocess import load_and_preprocess


def train_models(csv_path):
    X, y = load_and_preprocess(csv_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {}

    for target in y.columns:

        model = LinearRegression()

        # train
        model.fit(X_train, y_train[target])

        # predict
        predictions = model.predict(X_test)

        # evaluation metrics
        mae = mean_absolute_error(y_test[target], predictions)
        r2 = r2_score(y_test[target], predictions)

        print(f"\nModel: {target}")
        print(f"MAE: {mae:.3f}")
        print(f"R2 Score: {r2:.3f}")

        models[target] = model

        # save model
        joblib.dump(model, f"backend/ml/{target}_model.pkl")

    print("\nTraining complete. Models saved.")

if __name__ == "__main__":
    train_models("data/survey_data.csv")