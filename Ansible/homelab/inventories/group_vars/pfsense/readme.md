Test Privilage escalation. 
```bash
ansible pfsense -m command -a "whoami" --become
```

```bash
ansible-vault encrypt Ansible/homelab/inventories/group_vars/pfsense/vault.yml 
ansible-vault edit Ansible/homelab/inventories/group_vars/pfsense/vault.yml --vault-password-file ~/.ansible/vault-password
```