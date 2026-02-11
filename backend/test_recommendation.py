from recommendation_engine import recommend_actions

user_input = {
    "electricity_kwh": 300,
    "transport_mode": "petrol",
    "transport_km": 500,
    "diet_type": "mixed",
    "meals_per_month": 90,
    "waste_kg": 20
}

recommendations = recommend_actions(user_input)

print("Recommended Actions (ranked by reduction):\n")

for i, rec in enumerate(recommendations, start=1):
    print(f"{i}. Action: {rec['action']} -> Reduction: {rec['reduction']:.2f} kg CO2")
