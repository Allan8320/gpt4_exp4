
import os
from datetime import datetime


def save_recommendations(user_profile, ranked_items, explanations):

    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(
        output_folder,
        "recommendations.txt"
    )

    with open(file_path, "a", encoding="utf-8") as file:

        file.write("\n" + "=" * 65 + "\n")
        file.write("PERSONALIZED RECOMMENDATION SYSTEM\n")
        file.write("=" * 65 + "\n")

        file.write(
            "Saved on: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n"
        )

        file.write("\nUSER PROFILE\n")
        file.write("-" * 65 + "\n")

        for key, value in user_profile.items():
            file.write(f"{key}: {value}\n")

        file.write("\nRANKED RECOMMENDATIONS\n")
        file.write("-" * 65 + "\n")

        for item in ranked_items:
            file.write(f"\nRank: {ranked_items.index(item) + 1}\n")
            file.write(f"Name: {item['name']}\n")
            file.write(f"Score: {item['score']}/100\n")
            file.write(f"Description: {item['description']}\n")
            file.write(f"Reason: {item['reason']}\n")

        file.write("\nEXPLANATIONS\n")
        file.write("-" * 65 + "\n")

        for item in explanations:
            file.write(
                f"\n{item['rank']}. {item['name']}\n"
            )
            file.write(item["explanation"] + "\n")

        file.write("\n" + "=" * 65 + "\n\n")

    return file_path


def display_save_message(file_path):

    print("\n========================================")
    print("       RECOMMENDATIONS SAVED")
    print("========================================")
    print("File location:", os.path.abspath(file_path))
    print("========================================")
