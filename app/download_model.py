import os
import requests
from tqdm import tqdm

MODEL_URL = "https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf"
MODEL_PATH = "model.gguf"

def download_model(url=MODEL_URL, output_path=MODEL_PATH):
    if os.path.exists(output_path):
        print("✅ Model already exists. Skipping download.")
        return

    print(f"⬇️  Downloading model from {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(output_path, 'wb') as f, tqdm(
            desc="Downloading",
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

if __name__ == "__main__":
    download_model()
