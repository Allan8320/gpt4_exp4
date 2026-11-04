
def collect_user_profile():

    print("\n========================================")
    print("  PERSONALIZED RECOMMENDATION SYSTEM")
    print("========================================")

    print("\nEnter your details:\n")

    name = input("Enter your name: ").strip()

    while True:
        try:
            age = int(input("Enter your age: "))
            if age > 0:
                break
            print("Age must be greater than zero.")
        except ValueError:
            print("Enter a valid age.")

    background = input("Educational/Professional background: ").strip()

    interests = input("Enter your interests (comma separated): ").strip()

    skill_level = input("Skill level (Beginner/Intermediate/Advanced): ").strip()

    preferred_category = input("Preferred category: ").strip()

    goal = input("What is your goal? ").strip()

    while True:
        try:
            number_of_recommendations = int(
                input("Number of recommendations required: ")
            )

            if number_of_recommendations > 0:
                break
            print("Enter a number greater than zero.")

        except ValueError:
            print("Enter a valid number.")

    user_profile = {
        "name": name,
        "age": age,
        "background": background,
        "interests": interests,
        "skill_level": skill_level,
        "preferred_category": preferred_category,
        "goal": goal,
        "number_of_recommendations": number_of_recommendations
    }

    return user_profile
