import pandas as pd

# Likert scale mapping
LIKERT_MAPPING = {
    "Definitely No": 1,
    "Probably No": 2,
    "Neutral": 3,
    "Probably Yes": 4,
    "Definitely Yes": 5
}

# Habit frequency mapping
HABIT_MAPPING = {
    "Never": 1,
    "Rarely": 2,
    "Sometimes": 3,
    "Often": 4,
    "Always": 5
}

# Climate concern mapping
CLIMATE_MAPPING = {
    "Not concerned": 1,
    "Slightly concerned": 2,
    "Moderately concerned": 3,
    "Very concerned": 4,
    "Extremely concerned": 5
}

# Frequency mappings
FOOD_ORDER_MAPPING = {
    "0": 0,
    "1–2": 2,
    "3–5": 4,
    "6+": 6
}

# Waste segregation mapping
WASTE_SEG_MAPPING = {
    "Yes": 1,
    "Sometimes": 0.5,
    "No": 0
}

# Past attempt mapping
PAST_ATTEMPT_MAPPING = {
    "Yes": 1,
    "No": 0
}


def load_and_preprocess(csv_path):

    df = pd.read_csv(csv_path)

    # Map habit frequency columns
    habit_columns = [
        "reduce_electricity_habit",
        "public_transport_habit",
        "veg_preference_habit",
        "plastic_reduction_habit"
    ]

    for col in habit_columns:
        if col in df.columns:
            df[col] = df[col].map(HABIT_MAPPING)

    # Map climate concern
    if "climate_concern" in df.columns:
        df["climate_concern"] = df["climate_concern"].map(CLIMATE_MAPPING)

    # Map food ordering frequency
    if "food_order_frequency" in df.columns:
        df["food_order_frequency"] = df["food_order_frequency"].map(FOOD_ORDER_MAPPING)

    # Map waste segregation
    if "waste_segregation" in df.columns:
        df["waste_segregation"] = df["waste_segregation"].map(WASTE_SEG_MAPPING)

    # Map past attempts
    if "past_attempt" in df.columns:
        df["past_attempt"] = df["past_attempt"].map(PAST_ATTEMPT_MAPPING)

    # Likert mapping for willingness targets
    target_cols = [
        "willing_electricity_reduction",
        "willing_transport_shift",
        "willing_diet_reduction",
        "willing_waste_reduction"
    ]

    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].map(LIKERT_MAPPING)

    # Separate features and targets
    X = df.drop(columns=target_cols)
    y = df[target_cols]

    # One-hot encode categorical columns
    categorical_cols = [
        "gender",
        "education_level",
        "occupation",
        "living_situation",
        "primary_transport_mode"
    ]

    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    return X_encoded, y