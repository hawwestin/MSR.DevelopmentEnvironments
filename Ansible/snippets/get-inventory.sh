export ANSIBLE_CONFIG=$PWD/ansible/ansible.cfg

ansible -i Ansible/inventory --list-hosts all
ansible -i Ansible/inventory --list-hosts homelab

# Or, to get the full inventory in YAML format:
ansible-inventory --list -y