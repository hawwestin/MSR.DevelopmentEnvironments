docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v config.yaml:/app/config.yaml \
  -e GEMINI_API_KEY=${GEMINI_API_KEY:-Here_add_your_api_key} \
  --add-host=host.docker.internal:host-gateway \
  --restart unless-stopped \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml --port 4000