#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

docker compose up -d --wait ollama

# Pull models from Ollama For 12GB VRAM
for model in qwen2.5-coder:7b llama3.1:8b gemma2:9b llama3.2:3b; do
  docker compose exec -T ollama ollama pull "$model"
done

# Pull models from Ollama For 4GB VRAM
for model in qwen2.5:1.5b llama3.2:1b; do
  docker compose exec -T ollama ollama pull "$model"
done

# Create a local model with 2GB VRAM limit
docker compose exec -T ollama ollama create qwen-2gb-dev -f /ModelFile

# List all models in Ollama
docker compose exec -T ollama ollama list