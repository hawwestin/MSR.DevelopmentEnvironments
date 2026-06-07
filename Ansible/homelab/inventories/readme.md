# Diagnostic

```bash
ansible -i Ansible/homelab/inventories/inventory.ini --list-hosts new
```

# ping
```bash
ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg ansible -i Ansible/homelab/inventories/inventory.ini new -m ping -u root -k
ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg ansible -i Ansible/homelab/inventories/inventory.ini vm_linux -m ping
```

# known hosts
```bash
ssh-keyscan -H 192.168.50.100 >> ~/.ssh/known_hosts
```


# host setup
```bash
ansible -i Ansible/homelab/inventories/inventory.ini new -m setup
```