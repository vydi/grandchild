import os
import requests

MODEL_URL = "https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf"
MODEL_PATH = "models/gemma-3n-e4b-it.Q4_K_M.gguf"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        os.makedirs("models", exist_ok=True)
        r = requests.get(MODEL_URL, stream=True)
        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Model downloaded.")

if __name__ == "__main__":
    download_model()
