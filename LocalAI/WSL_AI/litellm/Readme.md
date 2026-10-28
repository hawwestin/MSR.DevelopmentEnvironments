

# Quick start 
Remove containers from other docker compose. Name must be unique. 
```bash
docker container rm ollama
docker container rm open-webui
```

To start
```bash
docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d --wait postgres ollama

bash LocalAI/WSL_AI/litellm/setup-models.sh

docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d
```
To stop
```bash
docker compose -f LocalAI/WSL_AI/litellm/docker-compose.yml stop

```

# env local variables
Copy the committed `.env` template to `.env.local`, then replace the placeholder values with your own credentials and random keys. `.env.local` is ignored by Git; do not put real credentials in `.env`.
prepare file
```bash
cp -n LocalAI/WSL_AI/litellm/.env LocalAI/WSL_AI/litellm/.env.local
```

Before starting, ensure `.env.local` contains `LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`, and `POSTGRES_PASSWORD`. Generate separate random values for the master key, salt key, and database password with `openssl rand -hex 32`; prefix the master and salt keys with `sk-`. Use the hex output directly for `POSTGRES_PASSWORD` so it is safe inside `DATABASE_URL`. Keep this file private. The root `.gitignore` already excludes `.env.*` files. 
you can use openssl command to generate random passwords. 
```bash
openssl rand -hex 16
```

For the initial LiteLLM Admin UI login, set `UI_USERNAME` (defaults to `admin`) and `UI_PASSWORD` in `.env.local`; use a unique password rather than the template placeholder. If `UI_PASSWORD` is unset, LiteLLM accepts `LITELLM_MASTER_KEY` as the UI password. These environment credentials provide shared admin bootstrap access; they are separate from OpenAI API keys and are not a Postgres login. After signing in at `http://localhost:4000/ui`, create and test a named `proxy_admin` account under Internal Users. Once that DB-backed account works, you can disable environment credential login with `general_settings.disable_env_credential_login: true` in `config.yml` and restart LiteLLM. Do not disable it before creating and verifying the database-backed account.

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

When you exit the settings and click the model list in a new chat, you will see **local-qwen-2gb**, **local-qwen2.5-0.5b**, **local-qwen2.5-1.5b**, and **local-llama3.2-1b** served by LiteLLM. Gemini is currently disabled in `config.yml` and is not listed.

## Reconfigure or add Ollama models

There are two names involved: the Ollama model tag, which must exist in Ollama, and the LiteLLM `model_name`, which is the alias shown to OpenWebUI and sent in API requests.

To make a model available, add its Ollama tag to the pull loop in `setup-models.sh` (or add an `ollama create` command there when using a custom Modelfile), then run the script. It starts Ollama, pulls the listed tags, and creates `qwen-2gb-dev`:

```bash
bash LocalAI/WSL_AI/litellm/setup-models.sh
```

Add a matching entry under `model_list` in `config.yml`. For example, to expose an Ollama tag named `mistral:7b`:

```yaml
model_list:
    - model_name: local-mistral-7b
        litellm_params:
            model: ollama/mistral:7b
            api_base: "http://ollama:11434"
```

Keep `api_base` as `http://ollama:11434` for Compose networking. Give every LiteLLM alias a unique `model_name`; the backend `model` must match the installed Ollama tag exactly. After editing `config.yml`, restart LiteLLM and refresh the model list in OpenWebUI:

```bash
docker compose --env-file LocalAI/WSL_AI/litellm/.env.local -f LocalAI/WSL_AI/litellm/docker-compose.yml up -d --force-recreate litellm
```


## Connectin LiteLLm to Gemini
https://aistudio.google.com/docs/get-started
https://ai.google.dev/gemini-api/docs/api-key