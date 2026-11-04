
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

ALLOWED_INTENTS = [
    "GENERATE_RECOMMENDATION",
    "REFINE_RECOMMENDATION",
    "SHOW_PROFILE",
    "EXPLAIN_RECOMMENDATION",
    "SAVE_RECOMMENDATION",
    "EXIT"
]


def detect_intent(user_message):

    prompt = f"""
You are an intent detection assistant.

Identify the user's intention from the message.

Possible intents:
{ALLOWED_INTENTS}

USER MESSAGE:
{user_message}

Return ONLY valid JSON in this format:
{{
    "intent": "REFINE_RECOMMENDATION",
    "reason": "The user wants to modify recommendations."
}}

Choose exactly one intent from the allowed list.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        detected = json.loads(result["response"])

        intent = detected.get("intent", "").upper()

        if intent not in ALLOWED_INTENTS:
            return {
                "intent": "GENERATE_RECOMMENDATION",
                "reason": "Fallback intent"
            }

        return {
            "intent": intent,
            "reason": detected.get("reason", "")
        }

    except requests.exceptions.RequestException as error:
        return {
            "intent": "ERROR",
            "reason": str(error)
        }

    except (ValueError, KeyError, TypeError):
        return {
            "intent": "ERROR",
            "reason": "Could not understand the AI response."
        }


def display_intent(result):

    print("\n========================================")
    print("          INTENT DETECTION")
    print("========================================")

    print("Detected Intent :", result["intent"])
    print("Reason          :", result["reason"])

    print("========================================")
