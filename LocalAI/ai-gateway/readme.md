# info
This is a demonstartion of stack that is mean to be installed on Proxmox VM to run 24/7.
Only liteLLm models without any self hosted due to hardware constrains. 

# Diagnostic
**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 

```bash
source LocalAi/ai-gateway/.env
# \/ imports 
export ANSIBLE_CONFIG=$PWD/LocalAI/ai-gateway/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/localAI-vault-password
```