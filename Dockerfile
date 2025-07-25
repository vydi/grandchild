FROM ubuntu:22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    git cmake build-essential wget curl libopenblas-dev libomp-dev python3 python3-pip \
    && apt-get clean

# Clone and build llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp
WORKDIR /app/llama.cpp
RUN cmake -DLLAMA_BUILD_SERVER=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Copy app files
WORKDIR /app
COPY app ./app
COPY requirements.txt .

# Install Python deps
RUN pip3 install --no-cache-dir -r requirements.txt

# Download the model (see: download_model.py)
RUN python3 app/download_model.py

# Expose server port
EXPOSE 8080

# Run server
CMD ["bash", "app/entrypoint.sh"]
