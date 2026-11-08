#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

docker compose up -d --wait ollama

# Models for 12GB VRAM
models_12gb=(
  qwen2.5-coder:7b # 28.05.2025
  llama3.1:8b # 30.11.2024
  gemma2:9b # 01.08.2024
  llama3.2:3b # 25.09.2024
  # Add more models here
)
for model in "${models_12gb[@]}"; do
  docker compose exec -T ollama ollama pull "$model"
done

# Models for 4GB VRAM
models_4gb=(qwen2.5:1.5b llama3.2:1b)
for model in "${models_4gb[@]}"; do
  docker compose exec -T ollama ollama pull "$model"
done

# Create a local model with 2GB VRAM limit
docker compose exec -T ollama ollama create qwen-2gb-dev -f /ModelFile

# List all models in Ollama
docker compose exec -T ollama ollama list