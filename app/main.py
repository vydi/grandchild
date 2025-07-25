from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
from datetime import datetime

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "/app/gemma-3n-e4b-it.Q4_K_M.gguf"
MEMORY_FILE = "/app/conversation_memory.json"
MAX_MEMORY = 20

class ChatInput(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_memory(messages):
    messages = messages[-MAX_MEMORY:]
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def format_prompt(history, new_input):
    convo = "\n".join([f"{m['sender']}: {m['text']}" for m in history])
    return f"{convo}\nYou: {new_input}\nGrandchild:" if convo else f"You: {new_input}\nGrandchild:"

@app.post("/chat")
async def chat(input: ChatInput):
    try:
        history = load_memory()
        history.append({"sender": input.userName, "text": input.prompt})

        prompt = format_prompt(history, input.prompt)

        cmd = [
            "llama-cli",
            "--model", MODEL_PATH,
            "--prompt", prompt,
            "--n-predict", "128",
            "--ctx-size", "2048",
            "--temp", "0.7"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            return {"error": f"Model error: {result.stderr.strip()}"}

        # Clean and capture output
        lines = result.stdout.strip().split("\n")
        reply = lines[-1] if lines else "Hmm, I’m not sure what to say."

        history.append({"sender": input.grandchildName, "text": reply})
        save_memory(history)

        return {"response": reply.strip()}

    except subprocess.TimeoutExpired:
        return {"error": "Model timed out."}
    except Exception as e:
        return {"error": str(e)}
