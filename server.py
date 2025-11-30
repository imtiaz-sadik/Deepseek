import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Get API key from environment variable for security
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# Replace with the actual Deepseek API endpoint and model
DEEPSEEK_URL = "https://api.deepseek.ai/v1/generate"  # check Deepseek docs for exact endpoint
DEEPSEEK_MODEL = "text-davinci"  # replace with the actual model name you want to use

app = Flask(__name__)
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
        "max_tokens": 500  # adjust as needed
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error if status code != 200
        data = response.json()
        # Adjust based on Deepseek response structure
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
    return "✅ AI Tutor Backend is running. Use /ask endpoint to chat."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT automatically
    print(f"🔥 AI Server is running at http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
