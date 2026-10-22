

# setup 
Remove containers from other docker compose. Name must be unique. 
```bash
docker container rm ollama
docker container rm open-webui
```

```bash
docker compose -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d --wait ollama
bash LocalAI/WSL_AI/litellm/setup-models.sh
docker compose -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d
```

## Connecting OpenWebUI to LiteLLM in WSL manual guide

We now need to configure OpenWebUI so it stops communicating directly with Ollama (or add LiteLLM as an additional source) and starts using your new router.

-  Log in to OpenWebUI (http://localhost:3000).

-  Click your profile icon in the bottom-left corner and go to Admin Panel -> Settings -> Connections tab.

- In the OpenAI API Connections section, click the + (Add) button.

- Configure the new connection:

    - API URL: [http://host.docker.internal:4000/v1](http://host.docker.internal:4000/v1)

    - API Key: sk-1234 (LiteLLM does not require authentication by default in local mode, but OpenWebUI requires entering something in this field).

- Click the refresh/save icon next to the added URL. A "Connected" message should appear.

- (Optional) If you want to test routing only through LiteLLM, disable the toggle next to the direct Ollama connection in the same tab.

When you exit the settings and click the model list in a new chat, you will see the names **gemini-1.5-flash** and **local-qwen-2gb** served from the unified LiteLLM endpoint. You can now expand config.yaml with load balancing, cost thresholds (budgets), or add other cloud providers without changing anything else in OpenWebUI.


## Connectin LiteLLm to Gemini
https://aistudio.google.com/docs/get-started
https://ai.google.dev/gemini-api/docs/api-key