
from flask import Flask, render_template, request, jsonify

from profile_module import analyze_user_profile
from prompt_module import construct_recommendation_prompt
from recommendation_module import generate_recommendations
from ranking_module import rank_recommendations
from explanation_module import generate_explanations
from feedback_module import refine_recommendation_prompt
from intent_module import detect_intent
from save_module import save_recommendations

app = Flask(__name__)

# Stores the current user's data for this local demo.
# This version is designed for one active user at a time.
user_profile = None
analysis = None
original_prompt = None
ranked_items = []
explanations = []


def generate_result(prompt):
    """Generate, rank and explain recommendations."""

    data = generate_recommendations(prompt)

    if "error" in data:
        return None, data["error"]

    if "recommendations" not in data:
        return None, "The AI did not return a valid recommendation list."

    ranked = rank_recommendations(data)

    if not ranked:
        return None, "No recommendations were generated."

    explanation_list = generate_explanations(
        ranked,
        user_profile
    )

    return {
        "recommendations": ranked,
        "explanations": explanation_list
    }, None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global user_profile, analysis
    global original_prompt, ranked_items, explanations

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Please provide your profile."}), 400

        required_fields = [
            "name", "age", "background", "interests",
            "skill_level", "preferred_category", "goal",
            "number_of_recommendations"
        ]

        for field in required_fields:
            if field not in data or str(data[field]).strip() == "":
                return jsonify({
                    "error": f"Please provide {field.replace('_', ' ')}."
                }), 400

        user_profile = {
            "name": str(data["name"]).strip(),
            "age": int(data["age"]),
            "background": str(data["background"]).strip(),
            "interests": str(data["interests"]).strip(),
            "skill_level": str(data["skill_level"]).strip(),
            "preferred_category": str(data["preferred_category"]).strip(),
            "goal": str(data["goal"]).strip(),
            "number_of_recommendations": int(
                data["number_of_recommendations"]
            )
        }

        if user_profile["age"] <= 0:
            return jsonify({"error": "Age must be greater than zero."}), 400

        if user_profile["number_of_recommendations"] <= 0:
            return jsonify({
                "error": "Number of recommendations must be greater than zero."
            }), 400

        analysis = analyze_user_profile(user_profile)

        original_prompt = construct_recommendation_prompt(
            user_profile,
            analysis
        )

        result, error = generate_result(original_prompt)

        if error:
            return jsonify({"error": error}), 500

        ranked_items = result["recommendations"]
        explanations = result["explanations"]

        return jsonify({
            "message": f"Welcome, {user_profile['name']}! Your recommendations are ready.",
            "profile": user_profile,
            "recommendations": ranked_items,
            "explanations": explanations
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid profile details."}), 400


@app.route("/chat", methods=["POST"])
def chat():
    global original_prompt, ranked_items, explanations

    if user_profile is None:
        return jsonify({
            "error": "Please submit your profile first."
        }), 400

    data = request.get_json()
    message = str(data.get("message", "")).strip() if data else ""

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    detected = detect_intent(message)
    intent = detected["intent"]

    if intent == "ERROR":
        return jsonify({
            "reply": "I could not understand your request. Please try again."
        })

    if intent == "SHOW_PROFILE":
        return jsonify({
            "reply": "Here is your saved profile.",
            "profile": user_profile
        })

    if intent == "EXPLAIN_RECOMMENDATION":
        return jsonify({
            "reply": "Here are the explanations for your recommendations.",
            "explanations": explanations
        })

    if intent == "SAVE_RECOMMENDATION":
        path = save_recommendations(
            user_profile,
            ranked_items,
            explanations
        )

        return jsonify({
            "reply": "Your recommendations have been saved successfully.",
            "saved_file": path
        })

    if intent == "EXIT":
        user_profile.clear()
        ranked_items = []
        explanations = []
        original_prompt = None

        return jsonify({
            "reply": "Thank you for using the Personalized Recommendation System. Goodbye!",
            "exit": True
        })

    if intent == "REFINE_RECOMMENDATION":
        refined_prompt = refine_recommendation_prompt(
            original_prompt,
            message
        )

        result, error = generate_result(refined_prompt)

        if error:
            return jsonify({"reply": error}), 500

        ranked_items = result["recommendations"]
        explanations = result["explanations"]

        return jsonify({
            "reply": "I have updated your recommendations based on your feedback.",
            "recommendations": ranked_items,
            "explanations": explanations
        })

    if intent == "GENERATE_RECOMMENDATION":
        result, error = generate_result(original_prompt)

        if error:
            return jsonify({"reply": error}), 500

        ranked_items = result["recommendations"]
        explanations = result["explanations"]

        return jsonify({
            "reply": "Here are your updated recommendations.",
            "recommendations": ranked_items,
            "explanations": explanations
        })

    return jsonify({
        "reply": "I could not identify that request. Please try again."
    })


if __name__ == "__main__":
    print("Starting Personalized Recommendation System...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)
