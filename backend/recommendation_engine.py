from scenario_engine import simulate_scenario


def recommend_actions(user_input):
    """
    Recommends emission reduction actions ranked by impact.
    Returns a list of dictionaries:
    [
        {"action": action_dict, "reduction": value},
        ...
    ]
    """

    # Define possible single actions
    possible_actions = [
        {"type": "reduce_electricity", "percent": 10},
        {"type": "reduce_electricity", "percent": 20},
        {"type": "change_transport", "new_mode": "public_transport"},
        {"type": "change_diet", "new_diet": "veg"}
    ]

    recommendations = []

    for action in possible_actions:
        # Simulate this single action
        result = simulate_scenario(user_input, [action])

        recommendations.append({
            "action": action,
            "reduction": result["reduction"]
        })

    # Sort by reduction (descending)
    recommendations.sort(key=lambda x: x["reduction"], reverse=True)

    return recommendations
