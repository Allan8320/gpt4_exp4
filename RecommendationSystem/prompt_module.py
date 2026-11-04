
def construct_recommendation_prompt(user_profile, analysis):

    prompt = f"""
You are an intelligent personalized recommendation assistant.

USER PROFILE:
Name: {user_profile['name']}
Age: {user_profile['age']}
Background: {user_profile['background']}
Interests: {user_profile['interests']}
Skill Level: {analysis['skill_level']}
Primary Interest: {analysis['primary_interest']}
Secondary Interest: {analysis['secondary_interest']}
Goal: {analysis['goal']}
Preferred Category: {analysis['preference']}

TASK:
Generate {user_profile['number_of_recommendations']}
personalized recommendations.

For each recommendation provide:

1. Recommendation Name
2. Description
3. Reason for Recommendation
4. Suitability Score (0-100)

INSTRUCTIONS:
- Consider the user's interests.
- Match recommendations to the user's skill level.
- Focus on the user's learning goal.
- Respect the preferred category.
- Rank recommendations from highest to lowest suitability.
- Provide practical and relevant suggestions.
- Avoid repeating recommendations.

Return the recommendations in a clear and structured format.
"""

    return prompt


def display_prompt(prompt):

    print("\n========================================")
    print("        GENERATED AI PROMPT")
    print("========================================")

    print(prompt)

    print("========================================")
