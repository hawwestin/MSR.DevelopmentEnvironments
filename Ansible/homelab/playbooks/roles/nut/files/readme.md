# Legacy role-local vault files
The role now renders `/etc/nut/upsd.users` from `templates/upsd.users.j2`. Its password variables are expected in `inventories/group_vars/all/vault.yml`; `users.vault` and `users.vault.exmaple` are not deployed by the role.

Do not decrypt or commit passwords as plaintext. Maintain inventory secrets with `ansible-vault` and use the repository's configured vault password workflow.

# snippet
```bash
EDITOR=nano  ansible-vault encrypt Ansible/homelab/playbooks/roles/nut/files/users.vault
EDITOR=nano  ansible-vault view Ansible/homelab/playbooks/roles/nut/files/users.vault
EDITOR=nano  ansible-vault edit Ansible/homelab/playbooks/roles/nut/files/users.vault
```