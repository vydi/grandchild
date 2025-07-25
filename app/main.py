from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess

app = FastAPI()
MODEL_PATH = "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf"

class ChatRequest(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    prompt = f"{request.userName}: {request.prompt}\n{request.grandchildName}:"
    try:
        result = subprocess.run(
            ["./llama.cpp/build/bin/llama-cli", "-m", MODEL_PATH, "-p", prompt, "-n", "100"],
            capture_output=True, text=True, check=True
        )
        return {"response": result.stdout.strip().split(f"{request.grandchildName}:")[-1].strip()}
    except Exception as e:
        return {"error": str(e)}
