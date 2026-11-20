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

ansible-inventory --host 192.168.50.1 
```

# use  ssh-agent
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_windows
ssh-add ~/.ssh/id_ansible
ssh-add ~/.ssh/id_pfsense # TODO 
ssh-add -l
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
Create private .env.proxmox file with Real secrets 
```bash
source Ansible/homelab/inventories/.env.proxmox
ansible-inventory -i Ansible/homelab/inventories/proxmox.proxmox.yml --graph
ansible-inventory -i Ansible/homelab/inventories/proxmox.proxmox.yml --list

ansible -i Ansible/homelab/inventories/proxmox.proxmox.yml all -m ping
```