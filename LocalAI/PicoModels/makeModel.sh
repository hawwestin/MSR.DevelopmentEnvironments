#!/bin/bash

# Check GPU status
nvidia-smi

# Install dependencies
sudo apt-get update
sudo apt-get install zstd
curl -fsSL https://ollama.com/install.sh | sh

ollama --version


# Set environment variable for Ollama service to limit VRAM usage
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo -e "[Service]\nEnvironment=\"OLLAMA_MAX_VRAM=2147483648\"" | sudo tee /etc/systemd/system/ollama.service.d/override.conf


sudo systemctl daemon-reload
sudo systemctl restart ollama

# Create small model for testing
ollama create qwen-2gb-dev -f Modelfile
ollama list


# Run the model
ollama run qwen-2gb-dev



# Ultra-lekki model z dobrą obsługą języka polskiego:
ollama run qwen2.5:0.5b

# Najlepszy kompromis jakości do rozmiaru (1.5B):
ollama run qwen2.5:1.5b

# Oficjalny mały model od Mety:
ollama run llama3.2:1b