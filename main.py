from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")  # set this in Render dashboard
HF_MODEL = "google/gemma-3n-e2b-it"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

app = FastAPI()

class ChatRequest(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Construct system + user prompt as message format
    messages = [
        {
            "role": "system",
            "content": [{
                "type": "text",
                "text": (
                    f"You are {request.grandchildName}, the cheerful and caring grandchild of {request.userName}. "
                    "Speak clearly, warmly, and with gentle humour. Keep responses short and empathetic. "
                    "You remember what Grandma tells you. If you don’t know something, be honest."
                )
            }]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": request.prompt}]
        }
    ]

    try:
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": messages})
        response.raise_for_status()
        result = response.json()
        
        # Hugging Face API typically returns a list of strings or dict
        if isinstance(result, list) and len(result) > 0:
            return {"response": result[0].get("generated_text", "").strip()}
        elif isinstance(result, dict) and "error" in result:
            return {"error": result["error"]}
        else:
            return {"response": str(result)}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
