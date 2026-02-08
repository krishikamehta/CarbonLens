from carbon_calculator import calculate_total_footprint

test_input = {
    "electricity_kwh": 300,
    "transport_mode": "petrol",
    "transport_km": 500,
    "diet_type": "mixed",
    "meals_per_month": 90,
    "waste_kg": 20
}

result = calculate_total_footprint(test_input)

print("Carbon Footprint Breakdown:")
for key, value in result.items():
    print(f"{key}: {value:.2f} kg CO2")
