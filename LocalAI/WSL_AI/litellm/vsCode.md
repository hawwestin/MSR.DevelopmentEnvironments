# General
Connect Local Models via LiteLLM to VS code to improve local development expirience. 

Example config for `Continue - Codestral, Claude, and more` Plugin
```json
"models": [
  {
    "title": "LiteLLM - Qwen 7B",
    "provider": "openai",
    "model": "local-qwen2.5-coder-7b",
    "apiKey": "sk-1234",
    "apiBase": "http://localhost:4000/v1"
  }
],
"tabAutocompleteModel": {
  "title": "LiteLLM - Autocomplete",
  "provider": "openai",
  "model": "local-qwen2.5-coder-7b",
  "apiKey": "sk-1234",
  "apiBase": "http://localhost:4000/v1"
}
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