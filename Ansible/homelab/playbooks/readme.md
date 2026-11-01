

# Playbooks 

```bash
ansible-playbook  Ansible/homelab/playbooks/ha_Hacs.yml 
```

Test syntax
```bash
ansible-playbook  Ansible/homelab/playbooks/ha_Hacs.yml --syntax-check
 ```
 If it reply with playbook name then all good.


Create dedicated user on remote 
```bash
ansible-playbook  playbooks/bootstrap_ansible_mgr.yml \
-e ansible_mgr_password_plain='your_root_password' \
-e ansible_mgr_ssh_pub_key="$(cat ~/.ssh/id_ansible.pub)" \
-K

ansible-playbook Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml --list-hosts

ansible-playbook Ansible/homelab/playbooks/bootstrap_ansible_mgr.yml
```


Other plays
```bash
ansible-playbook Ansible/homelab/playbooks/ha_otbr.yml --syntax-check
ansible-playbook Ansible/homelab/playbooks/docker_install.yml --syntax-check


ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit opti3040 --check
```

nut backup
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_windows

export ANSIBLE_CONFIG="$PWD/Ansible/homelab/ansible.cfg"
ansible-playbook \
  -i Ansible/homelab/inventories/hosts.ini \
  Ansible/homelab/playbooks/fetch_nut_snapshot.yml \
  --limit proxmox \
  -e "nut_snapshot_id=$(date -u +%Y%m%dT%H%M%SZ)"

```