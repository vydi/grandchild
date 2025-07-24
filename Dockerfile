FROM ubuntu:22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    git build-essential cmake wget curl libopenblas-dev libomp-dev \
    && apt-get clean

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app
WORKDIR /app

# Build llama-server
RUN cmake -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Create models directory and download model from GCS
RUN mkdir -p /app/models && \
    curl -o /app/models/gemma-3n-e4b-it.Q4_K_M.gguf https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf

# Expose port
EXPOSE 8080

# Run the model server
CMD ["/app/build/bin/llama-server", "-m", "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf", "--port", "8080"]
