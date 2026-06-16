from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Gemini API Configuration
load_dotenv()
# Store your API key in environment variable: GEMINI_API_KEY
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Recommendation Generator
def generate_recommendation(
    dietary_preferences,
    fitness_goal,
    dietary_restrictions,
    health_conditions,
    user_query,
):
    prompt = f"""
    Create a personalized fitness plan.

    Dietary Preferences: {dietary_preferences}
    Fitness Goal: {fitness_goal}
    Dietary Restrictions: {dietary_restrictions}
    Health Conditions: {health_conditions}
    User Query: {user_query}

    IMPORTANT:
    - Use very simple English.
    - Write as if explaining to a beginner.
    - Avoid medical, scientific, or technical terms.
    - Keep each recommendation short and easy to understand.
    - Use common food names and simple workout names.
    - Make recommendations practical and affordable.
    - Do not use difficult vocabulary.

    Return EXACTLY in this format with no extra text before or after:

    Diet Recommendations
    1.
    2.
    3.
    4.
    5.

    Workout Options
    1.
    2.
    3.
    4.
    5.

    Breakfast Ideas
    1.
    2.
    3.
    4.
    5.

    Dinner Options
    1.
    2.
    3.
    4.
    5.

    Useful Snacks
    1.
    2.
    3.
    4.
    5.

    Supplements
    1.
    2.
    3.
    4.
    5.

    Hydration Tips
    1.
    2.
    3.
    4.
    5.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return ""


def parse_recommendations(recommendations_text):
    """Parse the AI response into structured sections."""
    recommendations = {
        "diet_types": [],
        "workouts": [],
        "breakfasts": [],
        "dinners": [],
        "useful_snacks": [],
        "supplements": [],
        "hydration": [],
    }

    current_section = None

    for line in recommendations_text.splitlines():
        line = line.strip()
        if not line:
            continue

        lower = line.lower()

        if "diet recommendations" in lower:
            current_section = "diet_types"
        elif "workout options" in lower:
            current_section = "workouts"
        elif "breakfast ideas" in lower:
            current_section = "breakfasts"
        elif "dinner options" in lower:
            current_section = "dinners"
        elif "useful snacks" in lower:
            current_section = "useful_snacks"
        elif "supplements" in lower:
            current_section = "supplements"
        elif "hydration tips" in lower:
            current_section = "hydration"
        elif current_section:
            cleaned = line.lstrip("0123456789.-•* ").strip()
            if cleaned:
                recommendations[current_section].append(cleaned)

    return recommendations


# Load Home Page
@app.route("/")
def index():
    return render_template("index.html")


# Recommendation Page (POST)
@app.route("/recommendation", methods=["POST"])
def recommendations():
    dietary_preferences = request.form.get("dietary_preferences", "").strip()
    fitness_goal = request.form.get("fitness_goal", "").strip()
    dietary_restrictions = request.form.get("dietary_restrictions", "").strip()
    health_conditions = request.form.get("health_conditions", "").strip()
    user_query = request.form.get("user_query", "").strip()

    # Basic validation
    if not all([dietary_preferences, fitness_goal, dietary_restrictions,
                health_conditions, user_query]):
        return render_template("index.html", error="Please fill in all required fields.")

    recommendations_text = generate_recommendation(
        dietary_preferences,
        fitness_goal,
        dietary_restrictions,
        health_conditions,
        user_query,
    )

    if not recommendations_text:
        return render_template("index.html",
                               error="Could not generate recommendations. Please try again.")

    parsed = parse_recommendations(recommendations_text)

    return render_template(
        "suggestion_page.html",
        recommendations=parsed,
        fitness_goal=fitness_goal,
        dietary_preferences=dietary_preferences,
    )


if __name__ == "__main__":
    app.run(debug=True)
