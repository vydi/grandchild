# hf_proxy.py
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
HF_ENDPOINT = os.getenv("HF_ENDPOINT")  # Set this in Render or locally
HF_TOKEN = os.getenv("HF_TOKEN")        # Your Hugging Face personal access token

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    user = data.get("userName", "User")
    assistant = data.get("grandchildName", "Sam")

    full_prompt = f"You are {assistant}, a friendly and helpful grandchild talking to {user}. {prompt}"

    try:
        response = requests.post(HF_ENDPOINT, headers=headers, json={"inputs": full_prompt})
        result = response.json()
        if isinstance(result, list):
            output = result[0].get("generated_text", "")
        else:
            output = result.get("generated_text", "")
        return jsonify({"response": output.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
