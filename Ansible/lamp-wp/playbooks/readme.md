# ansible config 
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 
```bash
export ANSIBLE_CONFIG=$PWD/Ansible/lamp-wp/ansible.cfg
```

# Playbooks

**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:

```bash
export ANSIBLE_CONFIG=$PWD/Ansible/lamp-wp/ansible.cfg

# Run playbooks in order:
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/01-common.yml 
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/02-webserver.yml 
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/03-database.yml --ask-vault-pass
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/04-migration.yml --ask-vault-pass -vvv
```

## Notes
- All package management uses `raw` module (not `apt` module) to support Python 3.8
- All MySQL operations use `raw` module (not `mysql_*` modules) to support Python 3.8
- Playbooks 01-03 are fully tested and working on Ubuntu 20.04 with Python 3.8