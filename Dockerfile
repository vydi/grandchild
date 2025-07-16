FROM python:3.10-slim

# Install required packages
RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir torch transformers accelerate flask

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Expose port (for Cloud Run)
ENV PORT=8080
CMD ["python", "main.py"]