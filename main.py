from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "google/gemma-3n-e2b-it"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

app = FastAPI()

# ✅ Enable CORS to allow frontend on GitHub Pages to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://vydi.github.io"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional root route
@app.get("/")
async def root():
    return {"message": "👋 This is the Grandchild Assistant API. Use POST /chat."}

class ChatRequest(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    print("🟢 Incoming request:", request.dict())

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

        if isinstance(result, list) and len(result) > 0:
            reply = result[0].get("generated_text", "").strip()
            print("✅ Reply:", reply)
            return {"response": reply}
        elif "error" in result:
            print("❌ HF API Error:", result["error"])
            return {"error": result["error"]}
        else:
            return {"response": str(result)}
    except requests.exceptions.RequestException as e:
        print("❌ RequestException:", str(e))
        return {"error": f"Request failed: {str(e)}"}
