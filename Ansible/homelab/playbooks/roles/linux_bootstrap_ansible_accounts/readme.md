
Proxmox
```bash

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-pve.yml --list-hosts
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-pve.yml --syntax-check
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-pve.yml --tags bootstrap_preflight --limit opti3040 

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-pve.yml --check --limit opti3040  --diff
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-pve.yml  --diff --limit opti3040

```

LXC 
```bash

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml --list-hosts
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml --syntax-check
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml --tags bootstrap_preflight --limit TestDebian 

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml --check --limit TestDebian  --diff
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml  --diff --limit TestDebian
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-lxc.yml  --diff --limit AnsibleForDevops

```

vm 
```bash

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-vm.yml --list-hosts
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-vm.yml --syntax-check
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-vm.yml --tags bootstrap_preflight --limit TestDebian 

ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-vm.yml --check --limit TestDebian  --diff
ansible-playbook Ansible/homelab/playbooks/bootstrap-ansible-vm.yml  --diff --limit TestDebian

```