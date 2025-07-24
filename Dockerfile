FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git build-essential cmake curl wget \
    libopenblas-dev libomp-dev \
    && apt-get clean

# Set work directory
WORKDIR /app

# Clone llama.cpp repo and checkout stable version
RUN git clone https://github.com/ggerganov/llama.cpp.git
WORKDIR /app/llama.cpp

# Build llama-server
RUN cmake -DLLAMA_BUILD_SERVER=ON -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Go back and copy only what's needed
WORKDIR /app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Download model from GCS at runtime (or mount volume if preferred)
ENV MODEL_URL=https://storage.googleapis.com/grandchild/gemma-3n-e4b-it.Q4_K_M.gguf

# Expose default port
EXPOSE 8080

# Start server
CMD ["./entrypoint.sh"]
