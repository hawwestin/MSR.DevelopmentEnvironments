

# Playbooks 

```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/ha_Hacs.yml 
```

Test syntax
```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/ha_Hacs.yml --syntax-check
 ```
 If it reply with playbook name then all good.


Create dedicated user on remote 
```bash
ansible-playbook -i inventories/hosts.ini playbooks/bootstrap_ansible_mgr.yml \
-e ansible_mgr_password_plain='your_root_password' \
-e ansible_mgr_ssh_pub_key="$(cat ~/.ssh/id_ansible.pub)" \
-K


ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg ansible-playbook -i Ansible/homelab/inventories/inventory.ini Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml -k
```