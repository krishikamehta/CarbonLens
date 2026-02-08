import pandas as pd

_EMISSION_FACTORS = None


def load_emission_factors():
    """
    Loads emission factors from the CSV file and caches them.
    Returns a pandas DataFrame.
    """
    global _EMISSION_FACTORS

    if _EMISSION_FACTORS is None:
        _EMISSION_FACTORS = pd.read_csv("data/emission_factors.csv")

    return _EMISSION_FACTORS


def _get_emission_factor(category, sub_category):
    """
    Helper function to fetch the emission factor for a given category
    and sub-category from the emission factors table.
    """
    factors = load_emission_factors()

    row = factors[
        (factors["category"] == category) &
        (factors["sub_category"] == sub_category)
    ]

    if row.empty:
        raise ValueError(f"No emission factor found for {category} - {sub_category}")

    return float(row["co2_per_unit"].values[0])


def calculate_electricity_emissions(kwh):
    """
    Calculates CO2 emissions from electricity usage.
    """
    factor = _get_emission_factor("electricity", "grid")
    return kwh * factor


def calculate_transport_emissions(mode, km):
    """
    Calculates CO2 emissions from transport usage.
    """
    factor = _get_emission_factor("transport", mode)
    return km * factor


def calculate_food_emissions(diet_type, meals):
    """
    Calculates CO2 emissions from food consumption.
    """
    factor = _get_emission_factor("food", diet_type)
    return meals * factor


def calculate_waste_emissions(kg):
    """
    Calculates CO2 emissions from waste generation.
    """
    factor = _get_emission_factor("waste", "mixed")
    return kg * factor


def calculate_total_footprint(user_input):
    """
    Calculates category-wise and total household carbon footprint.

    user_input format:
    {
        "electricity_kwh": number,
        "transport_mode": string,
        "transport_km": number,
        "diet_type": string,
        "meals_per_month": number,
        "waste_kg": number
    }
    """

    electricity_emissions = calculate_electricity_emissions(
        user_input["electricity_kwh"]
    )

    transport_emissions = calculate_transport_emissions(
        user_input["transport_mode"],
        user_input["transport_km"]
    )

    food_emissions = calculate_food_emissions(
        user_input["diet_type"],
        user_input["meals_per_month"]
    )

    waste_emissions = calculate_waste_emissions(
        user_input["waste_kg"]
    )

    total_emissions = (
        electricity_emissions +
        transport_emissions +
        food_emissions +
        waste_emissions
    )

    return {
        "electricity": electricity_emissions,
        "transport": transport_emissions,
        "food": food_emissions,
        "waste": waste_emissions,
        "total": total_emissions
    }
