from flask import Flask, render_template, request
import google.generativeai as genai
import os

#set API key
os.environ["GOOGLE_API_KEY"] = " ENTER YOUR GOOGLE API KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)

#iintialize the model
model = genai.GenerativeModel("models/gemini-2.5-flash")

#custom function
def generate_recommendation(dietary_preferences, fitness_goal, dietary_restrictions, health_conditions, user_query):
    prompt = f"""
        Can you suggest a comprehensive plan that includes diet and workout options for better fitness?
        for this user:
        dietary preferences: {dietary_preferences},
        fitness goals: {fitness_goal},
        dietary restrictions: {dietary_restrictions},
        health conditions: {health_conditions},
        user query: {user_query},

        Based on the above user’s dietary preferences, fitness goals, dietary restrictions, and health conditions provided, create a customized plan that includes:

        Diet Recommendations: RETURN LIST
        5 specific diet types suited to their preferences and goals in short and user friendly language.

        Workout Options: RETURN LIST
        5 workout recommendations that align with their fitness level and goals in short and user friendly language.

        Meal Suggestions: RETURN LIST
        5 breakfast ideas in short and user friendly language.

        5 dinner options in short and user friendly language.

        Additional Recommendations: RETURN LIST
        Any useful snacks, supplements, or hydration tips tailored to their profile in short and user friendly language.
        mentain this sequence diet types ,workouts, breakfast, dinner, usefull snacks, supplement, hydration tips.
        """

    response = model.generate_content(prompt)
    return response.text if response else "No response from the model."




@app.route('/')
def index():
    return render_template('index.html', recommendations=None)

@app.route("/recommendation", methods=['POST'])
def recommendations():
    if request.method == "POST":
        #collect form data
        dietary_preferences = request.form['dietary_preferences']
        fitness_goal = request.form['fitness_goal']
        dietary_restrictions = request.form['dietary_restrictions']
        health_conditions = request.form['health_conditions']
        user_query = request.form['user_query']

        # Generate recommendations using the model
        recommendations_text = generate_recommendation(
            dietary_preferences, fitness_goal, dietary_restrictions, health_conditions, user_query
        )

        # Parse the results for display
        # Initialize dictionary
        recommendations = {
            "diet_types": [],
            "workouts": [],
            "breakfasts": [],
            "dinners": [],
            "useful_snacks": [],
            "supplements": [],
            "hydration": []
        }

        # Track current section
        current_section = None

        for line in recommendations_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Section headers
            if "Diet Recommendations" in line:
                current_section = "diet_types"
            elif "Workout Options" in line:
                current_section = "workouts"
            elif "Breakfast Ideas" in line:
                current_section = "breakfasts"
            elif "Dinner Options" in line:
                current_section = "dinners"
            elif "Useful Snacks" in line:
                current_section = "useful_snacks"
            elif "Supplements" in line:
                current_section = "supplements"
            elif "Hydration Tips" in line:
                current_section = "hydration"
            else:
                if current_section:
                    # Remove numbering if present
                    line = line.lstrip("0123456789. ").strip()
                    recommendations[current_section].append(line)

        print("dict :",recommendations)
        return render_template('suggestion_page.html', recommendations=recommendations)
#python main
if __name__=="__main__":

    app.run(debug=True)
