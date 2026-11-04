
def rank_recommendations(recommendations):

    if "error" in recommendations:
        return []

    items = recommendations["recommendations"]

    # Sort recommendations by score in descending order
    ranked_items = sorted(
        items,
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked_items


def display_rankings(ranked_items):

    print("\n========================================")
    print("        RECOMMENDATION RANKING")
    print("========================================")

    print(f"{'Rank':<10}{'Recommendation':<35}{'Score'}")
    print("-" * 60)

    for index, item in enumerate(ranked_items, start=1):

        print(
            f"{index:<10}"
            f"{item['name']:<35}"
            f"{item['score']}/100"
        )
