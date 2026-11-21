# General
Connect Local Models via LiteLLM to VS code to improve local development expirience. 
https://marketplace.visualstudio.com/items?itemName=Continue.continue 
Example config for `Continue - Codestral, Claude, and more` Plugin
```yaml
name: Local AI
version: 0.0.1
schema: v1

models:
  - name: Local Coding
    provider: openai
    model: local-qwen2.5-coder-7b
    apiBase: http://localhost:4000/v1
    apiKey: YOUR_LITELLM_KEY
    roles:
      - chat
      - edit
      - apply

  - name: Local General
    provider: openai
    model: local-gemma4-e4b
    apiBase: http://localhost:4000/v1
    apiKey: YOUR_LITELLM_KEY
    roles:
      - chat

  - name: Local Autocomplete
    provider: openai
    model: local-qwen2.5-coder-1.5b
    apiBase: http://localhost:4000/v1
    apiKey: YOUR_LITELLM_KEY
    roles:
      - autocomplete
      
  - name: Nomic Embed
    provider: openai
    model: nomic-embed-text:latest
    apiBase: http://localhost:4000/v1
    apiKey: YOUR_LITELLM_KEY
    roles:
      - embed
```

# official vs code extension from liteLLm
https://docs.litellm.ai/docs/tutorials/github_copilot_integration 

## Step 1: Build and install the extension
NPM install on windows
```powershell
winget install OpenJS.NodeJS.LTS
```


```powershell
git clone https://github.com/BerriAI/litellm.git
cd litellm/vscode-extension
npm ci
npm run package
code --install-extension litellm-vscode-0.1.0.vsix
```
## Step 2: Connect to your gateway

   1.  Run `Chat: Manage Language Models` from the Command Palette and pick LiteLLM
   2.  Enter a name for the connection, the gateway URL (for example https://litellm.example.com), and a LiteLLM API key: a virtual key, or on an SSO gateway the output of lite auth print-token (see the next section). The key is stored in VS Code's secret storage

The Language Models editor now lists the chat models that key can reach under the name you chose. Add LiteLLM again with another name to reach a second gateway or a second key.