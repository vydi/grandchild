FROM ubuntu:22.04

# Install required dependencies, including libcurl for CMake
RUN apt-get update && apt-get install -y \
    git cmake build-essential wget curl libcurl4-openssl-dev \
    libopenblas-dev libomp-dev clang \
    && apt-get clean

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp

# Set working directory
WORKDIR /app/llama.cpp

# Build llama.cpp without server or example binaries
RUN cmake -DLLAMA_BUILD_SERVER=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release -B build && \
    cmake --build build --config Release

# Set working directory for your app code
WORKDIR /app

# Copy app code
COPY . /app/

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Install Python dependencies
RUN apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r /app/requirements.txt

# Expose API port
EXPOSE 8080

# Run the entrypoint
CMD ["/app/entrypoint.sh"]
