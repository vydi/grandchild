FROM ubuntu:22.04

# Set environment
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone llama.cpp and build it
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp
WORKDIR /app/llama.cpp
RUN cmake -DLLAMA_BUILD_SERVER=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release -B build \
    && cmake --build build --config Release

# Set working directory for app
WORKDIR /app

# Copy all source files
COPY . /app/

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8080

# Start the server
ENTRYPOINT ["/app/entrypoint.sh"]
