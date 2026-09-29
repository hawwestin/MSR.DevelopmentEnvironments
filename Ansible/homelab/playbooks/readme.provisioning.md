# Playbooks for provisioning new hosts

Test syntax
```bash
ansible-playbook  Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml --syntax-check
 ```
If it reply with playbook name then all good.


Create dedicated user on remote. Provide variables if needed
```bash
ansible-playbook  playbooks/bootstrap_ansible_mgr.yml \
-e ansible_mgr_password_plain='your_root_password' \
-e ansible_mgr_ssh_pub_key="$(cat ~/.ssh/id_ansible.pub)" \
-K

```

Simple run this if we wnat use default variables 
```bash
ansible-playbook Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml --list-hosts

ansible-playbook Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml
```
