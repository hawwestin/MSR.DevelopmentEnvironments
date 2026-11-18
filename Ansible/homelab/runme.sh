#! /bin/bash
# This script is used to run the ansible playbook for the homelab environment.

# bash /mnt/c/repos/MSR.DevelopmentEnvironments/Ansible/homelab/runme.sh

cd '/mnt/c/repos/MSR.DevelopmentEnvironments'

source Ansible/homelab/.env
ansible-galaxy collection install -r requirements.yml

# ssh keys
eval "$(ssh-agent -s)"
ssh-add "$ANSIBLE_PRIVATE_KEY_FILE"
ssh-add -l

# Run ansible ping to test connectivity to sample hosts
ansible new -m ping

# enroll SSH host keys for the proxmox nodes
python3 Ansible/homelab/enroll-host-keys.py --dry-run
python3 Ansible/homelab/enroll-host-keys.py
# enroll SSH host keys for the VMs
# python3 Ansible/homelab/enroll-host-keys.py --group VM --inventory Ansible/homelab/inventories/inventory.ini --known-hosts "$HOME/.ssh/known_hosts"

ansible-playbook Ansible/homelab/playbooks/validate-ansible-access-passwordless.yml --limit new -e automation_validation_hosts=new 