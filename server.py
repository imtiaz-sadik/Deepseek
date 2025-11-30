import requests

API_KEY = "AIzaSyAkvX2qyIbjmk-uppwMPkPdokGqk__Y9wg"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

payload = {
    "contents": [{"parts": [{"text": "Explain electricity in simple words"}]}]
}

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": API_KEY
}

resp = requests.post(GEMINI_URL, json=payload, headers=headers)
print(resp.status_code, resp.text)