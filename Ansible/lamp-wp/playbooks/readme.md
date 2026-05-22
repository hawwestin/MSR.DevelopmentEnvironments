# config 
```bash
export ANSIBLE_CONFIG=$PWD/Ansible/lamp-wp/ansible.cfg
```
 # Playbooks

```bash
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/01-common.yml --ask-vault-pass
```