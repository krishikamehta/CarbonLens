from carbon_calculator import calculate_total_footprint


def apply_action(user_input, action):
    """
    Returns a modified copy of user_input after applying a single action.
    Does NOT modify the original dictionary.
    """
    # Create a copy to avoid mutating original input
    modified_input = user_input.copy()

    action_type = action.get("type")

    if action_type == "reduce_electricity":
        percent = action.get("percent", 0)
        reduction_factor = (100 - percent) / 100
        modified_input["electricity_kwh"] = (
            modified_input["electricity_kwh"] * reduction_factor
        )

    elif action_type == "change_transport":
        new_mode = action.get("new_mode")
        modified_input["transport_mode"] = new_mode

    elif action_type == "change_diet":
        new_diet = action.get("new_diet")
        modified_input["diet_type"] = new_diet

    else:
        raise ValueError(f"Unsupported action type: {action_type}")

    return modified_input


def simulate_scenario(user_input, actions):
    """
    Simulates a scenario by applying multiple actions to the user input.

    Returns:
    {
        "before": original_total,
        "after": new_total,
        "reduction": difference
    }
    """

    # Calculate original footprint
    original_result = calculate_total_footprint(user_input)
    original_total = original_result["total"]

    # Apply all actions sequentially
    modified_input = user_input.copy()
    for action in actions:
        modified_input = apply_action(modified_input, action)

    # Calculate new footprint
    new_result = calculate_total_footprint(modified_input)
    new_total = new_result["total"]

    reduction = original_total - new_total

    return {
        "before": original_total,
        "after": new_total,
        "reduction": reduction
    }
