

# setup 
Remove containers from other docker compose. Name must be unique. 
```bash
docker container rm ollama
docker container rm open-webui
```

Copy the committed `.env` template to `.env.local`, then replace the placeholder values with your own credentials and random keys. `.env.local` is ignored by Git; do not put real credentials in `.env`.

```bash
cp -n LocalAI/WSL_AI/litellm/.env LocalAI/WSL_AI/litellm/.env.local
```

```bash
docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d --wait postgres ollama
bash LocalAI/WSL_AI/litellm/setup-models.sh
docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d
```

Before starting, ensure `.env.local` contains `GEMINI_API_KEY`, `LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`, and `POSTGRES_PASSWORD`. Generate separate random values for the master key, salt key, and database password with `openssl rand -hex 32`; prefix the master and salt keys with `sk-`. Use the hex output directly for `POSTGRES_PASSWORD` so it is safe inside `DATABASE_URL`. Keep this file private. The root `.gitignore` already excludes `.env.*` files.

`LITELLM_OPENWEBUI_KEY` is optional. If unset, Open WebUI initially uses the master key. For regular use, create a virtual key in LiteLLM's Admin UI (`http://localhost:4000/ui`), set it as `LITELLM_OPENWEBUI_KEY` in `.env.local`, then run this from the repository root:

```bash
docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d --force-recreate open-webui
```

Keep the master key for administration only.

## Connecting OpenWebUI to LiteLLM in WSL manual guide

We now need to configure OpenWebUI so it stops communicating directly with Ollama (or add LiteLLM as an additional source) and starts using your new router.

-  Log in to OpenWebUI (http://localhost:3000).

-  Click your profile icon in the bottom-left corner and go to Admin Panel -> Settings -> Connections tab.

- In the OpenAI API Connections section, click the + (Add) button.

- Configure the new connection:

    - API URL: [http://litellm:4000/v1](http://litellm:4000/v1)

    - API Key: the LiteLLM virtual key configured for Open WebUI (or the master key for initial setup only).

- Click the refresh/save icon next to the added URL. A "Connected" message should appear.

- (Optional) If you want to test routing only through LiteLLM, disable the toggle next to the direct Ollama connection in the same tab.

When you exit the settings and click the model list in a new chat, you will see the names **gemini-1.5-flash** and **local-qwen-2gb** served from the unified LiteLLM endpoint. You can now expand config.yaml with load balancing, cost thresholds (budgets), or add other cloud providers without changing anything else in OpenWebUI.


## Connectin LiteLLm to Gemini
https://aistudio.google.com/docs/get-started
https://ai.google.dev/gemini-api/docs/api-key