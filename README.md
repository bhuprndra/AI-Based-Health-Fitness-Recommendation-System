# Health & Fitness Agent

AI-powered Health & Fitness Planner built with Flask and Google Gemini.

## Features
- Personalized diet recommendations
- Workout suggestions
- Breakfast and dinner ideas
- Healthy snack recommendations
- Supplement suggestions
- Hydration guidance
- Modern responsive UI

## Project Structure

```text
project/
│
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
│
├── templates/
│   ├── index.html
│   └── suggestion_page.html
│
├── static/
│   ├── style.css
│   └── image.png
│
└── .env
```

## Local Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a .env file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

5. Run

```bash
python app.py
```

## Deployment on Render

1. Push project to GitHub
2. Create a new Web Service on Render
3. Connect GitHub repository
4. Add environment variable:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

5. Deploy

Render uses render.yaml automatically.

## Security

Do not hardcode API keys in source code. Use environment variables.
