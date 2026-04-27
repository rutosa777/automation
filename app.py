from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("CLAUDE_API_KEY")

def ask_ai(text):
    if not API_KEY:
        return "ERROR: API key not set"

    try:
        res = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-3-haiku-20240307",
                "max_tokens": 300,
                "messages": [
                    {"role": "user", "content": text}
                ]
            },
            timeout=20
        )

        if res.status_code != 200:
            return f"API ERROR: {res.text}"

        data = res.json()
        return data["content"][0]["text"]

    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            result = "Please enter text"
        else:
            result = ask_ai(text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()