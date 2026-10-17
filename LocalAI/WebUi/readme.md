```bash
docker compose -f LocalAI/WebUi/docker-compose.yml up -d --wait ollama
bash LocalAI/WebUi/setup-models.sh
docker compose -f LocalAI/WebUi/docker-compose.yml up -d

```