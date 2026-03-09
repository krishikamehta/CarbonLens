from backend.scenario_engine import simulate_scenario
from backend.ml.predict import predict_adoption_probabilities


def recommend_actions(user_input, user_input_df):
    """
    user_input: dictionary used by scenario engine
    user_input_df: preprocessed dataframe used by ML model
    """

    # Possible actions to simulate
    possible_actions = [
        {"type": "reduce_electricity", "percent": 10},
        {"type": "reduce_electricity", "percent": 20},
        {"type": "change_transport", "new_mode": "public_transport"},
        {"type": "change_diet", "new_diet": "veg"}
    ]

    recommendations = []

    # Step 1: get ML adoption probabilities
    adoption_probs = predict_adoption_probabilities(user_input_df)

    for action in possible_actions:

        # Step 2: simulate emission reduction
        result = simulate_scenario(user_input, [action])

        reduction = result["reduction"]

        # Step 3: map action to probability category
        if action["type"] == "reduce_electricity":
            probability = adoption_probs["electricity"]

        elif action["type"] == "change_transport":
            probability = adoption_probs["transport"]

        elif action["type"] == "change_diet":
            probability = adoption_probs["diet"]

        else:
            probability = adoption_probs["waste"]

        # Step 4: compute final score
        final_score = reduction * probability

        recommendations.append({
            "action": action,
            "reduction": reduction,
            "adoption_probability": probability,
            "final_score": final_score
        })

    # Step 5: rank recommendations
    recommendations.sort(key=lambda x: x["final_score"], reverse=True)

    return recommendations