import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Get API key from environment variable for security
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# Replace with actual Deepseek API endpoint and model
DEEPSEEK_URL = "https://api.deepseek.ai/v1/generate"  # Check Deepseek docs
DEEPSEEK_MODEL = "text-davinci"  # Replace with desired model

app = Flask(__name__, static_folder="static")
CORS(app)

def ask_deepseek(prompt):
    if not API_KEY:
        return "❌ ERROR: Deepseek API key is missing in environment variables"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "prompt": prompt,
        "model": DEEPSEEK_MODEL,
        "max_tokens": 500
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "❌ ERROR: No answer returned by Deepseek")
    except requests.exceptions.RequestException as e:
        return f"❌ ERROR: {str(e)}"
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "")
    answer = ask_deepseek(user_prompt)
    return jsonify({"answer": answer})

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🔥 AI Server is running at http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
