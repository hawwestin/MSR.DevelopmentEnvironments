#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

docker compose up -d --wait ollama

for model in qwen2.5:0.5b qwen2.5:1.5b llama3.2:1b; do
  docker compose exec -T ollama ollama pull "$model"
done

docker compose exec -T ollama ollama create qwen-2gb-dev -f /ModelFile
docker compose exec -T ollama ollama list