#!/bin/bash
set -e

# Download model if not exists
MODEL_PATH="/app/gemma-3n-e4b-it.Q4_K_M.gguf"
if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading model from $MODEL_URL"
    curl -L "$MODEL_URL" -o "$MODEL_PATH"
fi

# Start the server
/app/llama.cpp/build/bin/llama-server -m "$MODEL_PATH" --port 8080
