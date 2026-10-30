EDITOR=nano  ansible-vault encrypt LocalAI/ai-gateway/group_vars/ai_gateway/vault.yml

EDITOR=nano  ansible-vault edit LocalAI/ai-gateway/group_vars/ai_gateway/vault.yml

EDITOR=nano  ansible-vault rekey LocalAI/ai-gateway/group_vars/ai_gateway/vault.yml  \
    --vault-password-file ~/.ansible/old-vault-password \
    --new-vault-password-file ~/.ansible/localAI-vault-password

EDITOR=nano  ansible-vault view LocalAI/ai-gateway/group_vars/ai_gateway/vault.yml