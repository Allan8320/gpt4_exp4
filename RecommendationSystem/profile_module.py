
def analyze_user_profile(user_profile):

    # Separate interests using comma
    interests = user_profile["interests"].split(",")

    # Remove unnecessary spaces
    cleaned_interests = []

    for interest in interests:
        cleaned_interests.append(interest.strip())

    # Identify primary and secondary interests
    primary_interest = cleaned_interests[0] if len(cleaned_interests) > 0 else "Not specified"

    secondary_interest = cleaned_interests[1] if len(cleaned_interests) > 1 else "Not specified"

    # Analyze skill level
    skill_level = user_profile["skill_level"]

    # Identify learning goal and preference
    goal = user_profile["goal"]
    preference = user_profile["preferred_category"]

    # Identify background and constraints
    background = user_profile["background"]
    age = user_profile["age"]

    analysis = {
        "primary_interest": primary_interest,
        "secondary_interest": secondary_interest,
        "skill_level": skill_level,
        "goal": goal,
        "preference": preference,
        "background": background,
        "age": age
    }

    return analysis


def display_profile_analysis(analysis):

    print("\n========================================")
    print("         PREFERENCE ANALYSIS")
    print("========================================")

    print("Primary Interest   :", analysis["primary_interest"])
    print("Secondary Interest :", analysis["secondary_interest"])
    print("Skill Level        :", analysis["skill_level"])
    print("Goal               :", analysis["goal"])
    print("Preference         :", analysis["preference"])
    print("Background         :", analysis["background"])
    print("Age                :", analysis["age"])

    print("========================================")
