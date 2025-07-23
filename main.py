from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import pipeline, AutoProcessor, AutoTokenizer, Gemma3nForConditionalGeneration

# Device config
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device}")

# Load model and processor
model_id = "google/gemma-3n-e2b-it"
model = Gemma3nForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32).eval().to(device)
processor = AutoProcessor.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# In-memory storage
conversation_history = {}

# FastAPI app
app = FastAPI()

class PromptRequest(BaseModel):
    userId: str
    userName: str
    grandchildName: str
    prompt: str

@app.post("/generate")
async def generate(request: PromptRequest):
    userId = request.userId
    userName = request.userName
    grandchildName = request.grandchildName
    prompt = request.prompt

    # Initialize history if not present
    if userId not in conversation_history:
        conversation_history[userId] = []

    history = conversation_history[userId]

    # Add new user prompt
    history.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    })

    # Build message chain
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text":
                f"You are {grandchildName}, the cheerful and caring grandchild of {userName}. "
                "Speak clearly, warmly, and with gentle humour. Keep responses short and empathetic. "
                "You remember what Grandma tells you. If you don’t know something, be honest."
            }]
        }
    ] + history

    try:
        prompt_text = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False
        )
        inputs = tokenizer(prompt_text, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
    except Exception as e:
        return {
            "error": f"Tokenization error: {str(e)}",
            "raw_prompt": prompt_text if 'prompt_text' in locals() else None
        }

    try:
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
        generated_ids = output[0][inputs["input_ids"].shape[-1]:]
        reply = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    except Exception as e:
        return {"error": f"Model generation failed: {str(e)}"}

    # Save assistant response
    history.append({
        "role": "assistant",
        "content": [{"type": "text", "text": reply}]
    })
    conversation_history[userId] = history

    return {"response": reply}
