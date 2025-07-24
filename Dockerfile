FROM ubuntu:22.04

# Install required dependencies, including compilers
RUN apt-get update && apt-get install -y \
    git build-essential cmake wget curl libopenblas-dev libomp-dev clang \
    && apt-get clean

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app
WORKDIR /app

# Build the server
RUN cmake -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Copy the model from GCS or your build context
RUN curl -o /app/models/gemma-3n-e4b-it.Q4_K_M.gguf https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf

# Expose the server port
EXPOSE 8080

# Run the llama server with the model
CMD ["/app/build/bin/llama-server", "-m", "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf", "--port", "8080"]
