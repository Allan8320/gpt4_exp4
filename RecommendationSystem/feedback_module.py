
def collect_feedback():

    print("\n========================================")
    print("          USER FEEDBACK")
    print("========================================")

    feedback = input(
        "\nWhich recommendations are useful? "
        "What would you like to change?\n"
        "Your feedback: "
    ).strip()

    return feedback


def refine_recommendation_prompt(
    original_prompt,
    feedback
):

    refined_prompt = f"""
{original_prompt}

USER FEEDBACK:
{feedback}

IMPORTANT INSTRUCTIONS:
1. Understand the user's feedback.
2. Remove recommendations that do not match the feedback.
3. Focus on the user's updated interests.
4. Respect the original skill level.
5. Generate a new personalized recommendation list.
6. Explain why each recommendation is suitable.
7. Provide suitability scores from 0 to 100.
8. Rank recommendations from highest to lowest.

Return ONLY valid JSON using this structure:

{{
    "recommendations": [
        {{
            "name": "Recommendation name",
            "description": "Description",
            "reason": "Reason for recommendation",
            "score": 95
        }}
    ]
}}
"""

    return refined_prompt
