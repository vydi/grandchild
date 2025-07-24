FROM ubuntu:22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    git build-essential cmake wget curl libopenblas-dev libomp-dev \
    && apt-get clean

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app
WORKDIR /app

# Build the server
RUN cmake -DLLAMA_BUILD_SERVER=ON -DLLAMA_BUILD_EXAMPLES=ON -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Copy your model into the image
COPY models /app/models

# Expose port 8080
EXPOSE 8080

# Run llama-server with your model
CMD ["/app/build/bin/llama-server", "-m", "/app/models/gemma-3n-e4b-it.Q4_K_M.gguf", "--port", "8080"]
