import os
import urllib.request

MODEL_URL = "https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf"
MODEL_PATH = "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf"

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("Downloading model from GCS...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download complete.")
else:
    print("Model already exists.")
