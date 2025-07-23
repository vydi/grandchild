from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    user: str
    assistant: str
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatInput):
    reply = f"Hi {data.user}, I’m {data.assistant}. You said: {data.message}"
    return {"reply": reply}
