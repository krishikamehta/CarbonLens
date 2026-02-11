from scenario_engine import simulate_scenario

original_input = {
    "electricity_kwh": 300,
    "transport_mode": "petrol",
    "transport_km": 500,
    "diet_type": "mixed",
    "meals_per_month": 90,
    "waste_kg": 20
}

actions = [
    {"type": "reduce_electricity", "percent": 20},
    {"type": "change_transport", "new_mode": "public_transport"},
    {"type": "change_diet", "new_diet": "veg"}
]

result = simulate_scenario(original_input, actions)

print("Scenario Simulation Result:")
print(f"Before: {result['before']:.2f} kg CO2")
print(f"After: {result['after']:.2f} kg CO2")
print(f"Reduction: {result['reduction']:.2f} kg CO2")
