# Diagnostic
**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 

```bash
source Ansible/lamp-wp/.env
# or load content
export ANSIBLE_CONFIG=$PWD/Ansible/lamp-wp/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/Lamp-vault-password

#test
ansible -i Ansible/lamp-wp/inventories/hosts.ini all -m ping
```


# project map
ansible/lamp-wp/
 ├── inventories/
 │    ├── hosts.ini
 │    ├── hosts_vars/
 │    └── group_vars/
 │        └── all.yml
 ├── roles/
 │    ├── common/          # apt update, base packets, timezone, firewall
 │    ├── webserver/       # Apache, configurable PHP (default 8.4), modules
 │    ├── mysql/           # MySQL 8.0.41, user, db
 │    └── wordpress/       # install WP, perms, wp-config
 ├── playbooks/
 │    ├── 01-common.yml
 │    ├── 02-webserver.yml
 │    ├── 03-database.yml
 │    └── 04-migration.yml
 ├── vault/
 │    └── secrets.yml (Encrypted)
 └── files/
      └── wordpress-6.9.4.tar.gz


# web server data

The deployment currently targets Ubuntu 22.04 and 24.04 and defaults to PHP 8.4 through the Ondrej PHP PPA. The host details below are a historical Ubuntu 20.04 / PHP 7.4 snapshot, not the current role configuration.
