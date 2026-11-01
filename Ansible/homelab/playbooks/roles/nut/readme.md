# General
Configuration of NUT Ups tools. Server and client roles.

# Homelab context
UPS is connected via USB to Rasppbery Pi. Other hosts like proxmox and Qnap Nas are clients to it. 
Proxmox configuration is as code driven by this ansible playbook. 
Qnap Nas have a hardcoded configuration in /etc/nut that are locked to change. So to connect UPS via Rasppbery we had to emulate those options as a proxy ups and re-create hardcoded crudentials for Qnap. 

Proxmox Cluster (3 nodes) have enable High Availability. Some lxc containers will be migrated in event of one box is down. Nut logic must handle this in case of power loss and disarm HA before we start of controled shutdown. Without it LXC can start migration in the middle of shutdown of all hosts. 

Ceph converged cluster on proxmox nodes also need a dedicated logic to perform controled shutdown 

Access to all hosts are via SSH-Keys with passphrase. It is a safety standard that always should be fallowed. Therefor only You can apply those playbook. In today era of AI it is must have to prevent agents from roaming on your homelab without your intent applying half baked playbooks and reconfiguring things that may not be protected by backup. 

# UPS and power usage
Today I measure power usage via smart plug on the wall before UPS. This gives me overall context about power usage in Office. Seecondary data stream are collected directly from UPS. All data are saved to Home Assistant so I have long term data. Home assistant also leave on proxmox cluster. 

# ideas
NUT can do more automations in the future. Today I just don't want to damage any host and its data. 

# TODO
- Proxmox Cluster HA management && Ceph converged clsuter management
    - Design and review Proxmox HA and Ceph shutdown coordination before enabling NUT monitor services or automatic shutdown behavior.
- Safely test callback conditions without triggering `upsmon -c fsd` or shutting down a host.
- Add appropriate monitor restart handling if and when `nut-monitor` is approved for activation.
- Document and manually review Proxmox play commands; run them only by the user with the passphrase-protected SSH key loaded in `ssh-agent`.


## Role Configuration
The role renders `nut.conf`, `upsmon.conf`, `upssched.conf`, and `upssched-cmd` on server and client hosts. The server additionally receives `ups.conf`, `upsd.conf`, and `upsd.users`. Passwords used by these templates belong in the inventory Ansible Vault file at `inventories/group_vars/all/vault.yml`; do not commit plaintext credentials.

Required Vault variables are `vault_nut_monitor_password`, `vault_nut_admin_password`, and `vault_nut_qnap_admin_password`. The QNAP `[admin]` compatibility account is retained, but its password is supplied through Vault.

The role currently stops and disables `nut-monitor`. Do not enable it or trigger the callback's forced-shutdown path until the Proxmox HA and Ceph shutdown coordination described above has been designed, tested safely, and explicitly approved. Proxmox/cluster playbooks are user-run only; an AI agent must not execute them.

For a Proxmox check-mode review, start `ssh-agent`, add the passphrase-protected key, then run this from the repository root:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_windows
export ANSIBLE_CONFIG="$PWD/Ansible/homelab/ansible.cfg"
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit proxmox --check --diff
```
Only run a non-check deployment after reviewing the diff and explicitly authorizing it.
