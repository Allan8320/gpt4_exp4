
def generate_explanations(ranked_items, user_profile):

    explanations = []

    for index, item in enumerate(ranked_items, start=1):

        explanation = (
            f"{item['name']} is suitable for "
            f"{user_profile['name']} because "
            f"{item['reason']} "
            f"It matches the user's interests in "
            f"{user_profile['interests']} and supports "
            f"the goal of {user_profile['goal']}. "
            f"It is recommended for the user's "
            f"{user_profile['skill_level']} skill level."
        )

        explanation_data = {
            "rank": index,
            "name": item["name"],
            "score": item["score"],
            "explanation": explanation
        }

        explanations.append(explanation_data)

    return explanations


def display_explanations(explanations):

    print("\n========================================")
    print("      RECOMMENDATION EXPLANATIONS")
    print("========================================")

    for item in explanations:

        print("\nRank:", item["rank"])
        print("Recommendation:", item["name"])
        print("Suitability Score:", item["score"], "/100")

        print("\nWhy is this suitable?")
        print(item["explanation"])

        print("-" * 60)
