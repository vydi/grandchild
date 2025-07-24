FROM ghcr.io/ggerganov/llama.cpp:latest

# Copy model into container
COPY ./models /models

# Expose the default server port
EXPOSE 8080

# Run the server with desired model and settings
CMD ["/app/server", "-m", "/models/gemma-3n-e4b-it.Q4_K_M.gguf", "--port", "8080", "--ctx-size", "2048"]
