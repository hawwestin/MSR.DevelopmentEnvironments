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

ansible -a "hostname" new

ansible new -m ping
```

# known hosts
```bash
ssh-keyscan -H 192.168.50.100 >> ~/.ssh/known_hosts
```


# host setup
```bash
ansible new -m setup
```