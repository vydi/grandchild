import os
import torch
from flask import Flask, request, jsonify
from transformers import AutoProcessor, Gemma3nForConditionalGeneration

HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_ID = "google/gemma-3n-e2b-it"

app = Flask(__name__)

model = Gemma3nForConditionalGeneration.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    token=HF_TOKEN
).eval()

processor = AutoProcessor.from_pretrained(MODEL_ID, token=HF_TOKEN)

@app.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    history = data.get("history", [])

    messages = [
        {"role": "system", "content": [{"type": "text", "text": "You are a loving adult grandchild speaking to your grandma. Be kind, curious, and helpful."}]}
    ]

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": [{"type": "text", "text": user_msg}]})
        messages.append({"role": "assistant", "content": [{"type": "text", "text": assistant_msg}]})
    messages.append({"role": "user", "content": [{"type": "text", "text": message}]})

    inputs = processor.apply_chat_template(messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        outputs = model.generate(**inputs, max_new_tokens=200, do_sample=True, temperature=0.7, top_p=0.9)
        output_ids = outputs[0][input_len:]

    response = processor.decode(output_ids, skip_special_tokens=True)
    return jsonify({"reply": response})
