
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_recommendations(prompt):

    print("\nConnecting to Ollama AI...")
    print("Generating personalized recommendations...\n")

    structured_prompt = prompt + """

IMPORTANT:
Return ONLY a valid JSON object.
Do not include markdown code blocks.

Use this exact structure:

{
  "recommendations": [
    {
      "name": "Recommendation name",
      "description": "Description",
      "reason": "Reason for recommendation",
      "score": 90
    }
  ]
}

Ensure score is a number between 0 and 100.
Return exactly the requested number of recommendations.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": structured_prompt,
                "stream": False,
                "format": "json"
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        ai_response = result["response"]

        recommendations = json.loads(ai_response)

        return recommendations

    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to Ollama."}

    except requests.exceptions.Timeout:
        return {"error": "AI response timed out."}

    except requests.exceptions.RequestException as error:
        return {"error": str(error)}

    except (KeyError, ValueError, TypeError):
        return {"error": "Invalid AI response."}


def display_recommendations(data):

    if "error" in data:
        print(data["error"])
        return

    print("\n========================================")
    print("       PERSONALIZED RECOMMENDATIONS")
    print("========================================")

    for item in data["recommendations"]:

        print("\nRecommendation:", item["name"])
        print("Description:", item["description"])
        print("Reason:", item["reason"])
        print("Score:", item["score"], "/100")
