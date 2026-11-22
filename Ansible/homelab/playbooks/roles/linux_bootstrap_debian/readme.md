LXC 
```bash

ansible-playbook Ansible/homelab/playbooks/linux_bootstrap_debian.yml --list-hosts
ansible-playbook Ansible/homelab/playbooks/linux_bootstrap_debian.yml --syntax-check
ansible-playbook Ansible/homelab/playbooks/linux_bootstrap_debian.yml --tags bootstrap_preflight --limit TestDebian 

ansible-playbook Ansible/homelab/playbooks/linux_bootstrap_debian.yml --check --limit TestDebian  --diff
ansible-playbook Ansible/homelab/playbooks/linux_bootstrap_debian.yml  --diff --limit TestDebian
ansible-playbook Ansible/homelab/playbooks/debian_maintenance.yml  --diff --limit TestDebian

```