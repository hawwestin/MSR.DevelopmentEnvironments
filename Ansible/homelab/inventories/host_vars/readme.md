```bash
# Encrypt both files
ansible-vault encrypt Ansible/homelab/inventories/hosts_vars/192.168.50.1/vault.yml
ansible-vault encrypt Ansible/homelab/inventories/hosts_vars/pve2/vault.yml
ansible-vault encrypt Ansible/homelab/inventories/hosts_vars/opti3040/vault.yml
ansible-vault encrypt Ansible/homelab/inventories/hosts_vars/opti3050/vault.yml

```

```bash
ansible-vault edit Ansible/homelab/inventories/hosts_vars/192.168.50.1/vault.yml --vault-password-file ~/.ansible/vault-password
ansible-vault edit Ansible/homelab/inventories/hosts_vars/pve2/vault.yml --vault-password-file ~/.ansible/vault-password
ansible-vault edit Ansible/homelab/inventories/hosts_vars/opti3040/vault.yml --vault-password-file ~/.ansible/vault-password
ansible-vault edit Ansible/homelab/inventories/hosts_vars/opti3050/vault.yml --vault-password-file ~/.ansible/vault-password

```