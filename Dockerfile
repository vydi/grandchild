FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y git cmake build-essential curl wget libopenblas-dev libomp-dev && apt-get clean

# Copy everything
COPY . .

# Clone and build llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp && \
    cd llama.cpp && \
    cmake -B build -DLLAMA_BUILD_EXAMPLES=ON -DLLAMA_BUILD_SERVER=ON && \
    cmake --build build --config Release

# Install Python deps
RUN pip install -r requirements.txt

# Download model
RUN python app/download_model.py

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
