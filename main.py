from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoProcessor, AutoTokenizer, Gemma3nForConditionalGeneration

# Model setup
device = "cuda" if torch.cuda.is_available() else "cpu"
model_id = "google/gemma-3n-e2b-it"
model = Gemma3nForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32).eval().to(device)
processor = AutoProcessor.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

app = FastAPI()

class ChatRequest(BaseModel):
    userName: str
    grandchildName: str
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text":
                f"You are {request.grandchildName}, the cheerful and caring grandchild of {request.userName}. "
                "Speak clearly, warmly, and with gentle humour. Keep responses short and empathetic. "
                "You remember what Grandma tells you. If you don’t know something, be honest."
            }]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": request.prompt}]
        }
    ]

    try:
        prompt_text = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False
        )
        inputs = tokenizer(prompt_text, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
        generated_ids = output[0][inputs["input_ids"].shape[-1]:]
        reply = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    except Exception as e:
        return {"error": str(e)}

    return {"response": reply}
