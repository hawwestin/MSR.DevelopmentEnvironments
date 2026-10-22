```bash
docker compose -f LocalAI/WSL_AI/ollamaWebUi/docker-compose.yml up -d --wait ollama
bash LocalAI/WSL_AI/ollamaWebUi/setup-models.sh
docker compose -f LocalAI/WSL_AI/ollamaWebUi/docker-compose.yml up -d

```


## nvidia drivers for WSL
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html 