# References
- https://docs.ansible.com/projects/ansible/latest/inventory_guide/intro_inventory.html

# Diagnostic
**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 

```bash
export ANSIBLE_CONFIG=$PWD/Ansible/homelab/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
```

```bash
ansible --list-hosts new

ansible new -m ping

ansible -a "hostname" new
```

# known hosts
```bash
ssh-keyscan -H 192.168.100.14 >> ~/.ssh/known_hosts
```
# 
```bash
ssh-copy-id -i ~/.ssh/id_ansible.pub ansible_mgr@192.168.100.100
ssh-copy-id -i ~/.ssh/id_rsa_windows.pub root@192.168.50.6
```


# host setup
```bash
ansible new -m setup
```

## Proxmox plugin
```bash
pipx inject ansible proxmoxer requests
pipx runpip ansible list

ansible-doc -t inventory community.proxmox.proxmox

ansible-galaxy collection install community.general
ansible-galaxy collection install community.proxmox
```
Provision ansible user on proxmxo server/cluster using [ansibleUserProxmox](MSR.DevelopmentEnvironments/Ansible/snippets/ansibleUserProxmox.sh)

```bash
source Ansible/homelab/inventories/.env.proxmox
ansible-inventory -i Ansible/homelab/inventories/proxmox.proxmox.yml --graph
ansible-inventory -i Ansible/homelab/inventories/proxmox.proxmox.yml --list

ansible -i Ansible/homelab/inventories/proxmox.proxmox.yml all -m ping
```