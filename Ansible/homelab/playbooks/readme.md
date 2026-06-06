# playbooks

```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/ha_Hacs.yml 
```

Test syntax
```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/ha_Hacs.yml --syntax-check
 ```
 If it reply with playbook name then all good.