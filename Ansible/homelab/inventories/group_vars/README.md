# Ansible Vault Setup

This directory contains encrypted group_vars files that store the `ansible_mgr` password for hosts using the `su` privilege escalation method.

## Setup Instructions

### 1. Create a vault password file (one-time setup)

```bash
# Create and save your vault password in a file (NOT in git)
echo "your-secret-vault-password" > ~/.ansible/vault-password
chmod 600 ~/.ansible/vault-password
```

### 2. Encrypt the group_vars files

use `--vault-password-file ~/.ansible/vault-password`
or set env variable
```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
```

```bash
# Encrypt both files
ansible-vault encrypt Ansible/homelab/inventories/group_vars/new/vault.yml 
ansible-vault encrypt Ansible/homelab/inventories/group_vars/vm_linux/vault.yml 
# and so on

# Edit to set the actual password
ansible-vault edit Ansible/homelab/inventories/group_vars/vm_linux/vault.yml --vault-password-file ~/.ansible/vault-password
ansible-vault edit Ansible/homelab/inventories/group_vars/new/vault.yml --vault-password-file ~/.ansible/vault-password
```

### 3. Use with ansible commands

```bash
# Set vault password file path in environment or use --vault-password-file flag
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password

# Now run commands without -K flag
ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg ansible -i Ansible/homelab/inventories/inventory.ini vm_linux -m ping
ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg ansible-playbook -i Ansible/homelab/inventories/inventory.ini Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml
```

### 4. Add to your shell profile (optional)

```bash
# Add to ~/.bashrc or ~/.zshrc
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
```

## Contents

- **vm_linux.yml** - Contains `ansible_become_password` for vm_linux group hosts
- **new.yml** - Contains `ansible_become_password` for new group hosts

Both files are encrypted and should never be committed to version control.
