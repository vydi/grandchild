from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

class ChatRequest(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

@app.post("/chat")
def chat(req: ChatRequest):
    model_path = "models/gemma-3n-e4b-it.Q4_K_M.gguf"
    if not os.path.exists(model_path):
        return {"error": "Model not found."}

    command = [
        "./llama.cpp/build/bin/llama-cli",
        "-m", model_path,
        "-p", req.prompt
    ]

    try:
        result = subprocess.check_output(command).decode("utf-8")
        return {"response": result.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}
