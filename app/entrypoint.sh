#!/bin/bash

# Optional: ensure the model exists locally before launching
if [ ! -f /app/model.gguf ]; then
    echo "Model not found. Downloading..."
    curl -L -o /app/model.gguf "https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf"
fi

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8080