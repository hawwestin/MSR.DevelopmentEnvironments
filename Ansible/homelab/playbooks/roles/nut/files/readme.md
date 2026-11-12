# Legacy role-local vault files
The role now renders `/etc/nut/upsd.users` from `templates/upsd.users.j2`. Its password variables are expected in `inventories/group_vars/all/vault.yml`; `users.vault` and `users.vault.exmaple` are not deployed by the role.

Do not decrypt or commit passwords as plaintext. Maintain inventory secrets with `ansible-vault` and use the repository's configured vault password workflow.

# snippet
```bash
EDITOR=nano  ansible-vault encrypt Ansible/homelab/playbooks/roles/nut/files/users.vault
EDITOR=nano  ansible-vault view Ansible/homelab/playbooks/roles/nut/files/users.vault
EDITOR=nano  ansible-vault edit Ansible/homelab/playbooks/roles/nut/files/users.vault
```

TODO ANSBILE for NUT server to orchetrate Proxmox orchestration. 
- Dedicated account on Proxmox host for ansible_nut
- RPI must trust known_hosts to all proxmox nodes. 
    - How to track if Known host cert was changed for proxmox and ansible will not connect to it ? 
    - Disable SSH-Key checking on RPI so this will not prevent us from NUT ansible orchestration ?
- ansible_nut SSH Key need to be distributed. What with passkay in this scenario ?
    - Distribution of Publish key we can orchestrate from WSL coordinator development. 
- Inventory 
    - We can use dynamic repository.. This uses PAM account and token. 
        - can this PAM account on cluster level orchestrate HA and ceph?