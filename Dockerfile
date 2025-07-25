FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    git build-essential cmake wget curl libopenblas-dev libomp-dev clang \
    && apt-get clean

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app
WORKDIR /app

# Disable Metal backend and build the server
RUN cmake -DLLAMA_METAL=OFF -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Download model from GCS
RUN mkdir -p /app/models && \
    curl -o /app/models/gemma-3n-e4b-it.Q4_K_M.gguf https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf

# Expose the llama server port
EXPOSE 8080

# Run llama-server with the model
CMD ["/app/build/bin/llama-server", "-m", "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf", "--port", "8080"]
