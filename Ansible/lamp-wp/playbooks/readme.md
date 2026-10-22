# Playbooks

**IMPORTANT:** Always set the ANSIBLE_CONFIG environment variable before running playbooks:
This fix issue with paths to ansible roles.
By default it looks for them under playbooks directory. 

```bash
export ANSIBLE_CONFIG=$PWD/Ansible/lamp-wp/ansible.cfg
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/Lamp-vault-password

# Run playbooks in order:
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/01-common.yml 
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/02-webserver.yml 
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/03-database.yml --ask-vault-pass
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/04-migrationweb.yml --ask-vault-pass -vvv
ansible-playbook -i Ansible/lamp-wp/inventories/hosts.ini Ansible/lamp-wp/playbooks/04-migrationdb.yml -vvv --ask-vault-pass 

```

## Notes
- Files used for restore are located in `\\fileserver.msr.loc\BlogBackups` 
- All package management uses `raw` module (not `apt` module) to support Python 3.8
- All MySQL operations use `raw` module (not `mysql_*` modules) to support Python 3.8
- Playbooks 01-03 are fully tested and working on Ubuntu 20.04 with Python 3.8

## Pre-requisites for migration
Copy latest Zip backup to `\\fileserver.msr.loc\BlogBackups` 

``` bash
# check
ls /mnt/BlogBackups/ -la
mount -av
# remount if not mounted > ignored
mount -t virtiofs BlogBackups /mnt/BlogBackups

cp /mnt/BlogBackups/moja_baza_backup_2026_10.sql /mnt/BlogBackups/Restore/dump.sql
```
Simple unzip
```bash
unzip -X /mnt/BlogBackups/html_2026_10.zip -d /mnt/BlogBackups/Restore/html
# or
7z x /mnt/BlogBackups/html_2026_05_01.zip -o/mnt/BlogBackups/Restore/html
```
more complex
```bash
# Install the package if you don't have it
sudo apt install libarchive-tools

# Extract and strip the top-level date folder
bsdtar -xf /mnt/BlogBackups/html_2026_10_01.zip -C /mnt/BlogBackups/Restore/html --strip-components=1
```

### check
size post migration
```bash
sudo du -sh /var/www/html/
sudo du -sh /mnt/BlogBackups/Restore/html/
```
Test if there is no /mnt/BlogBackups/Restore/html/html_{DATE} dated directory. as it will copy it to /var/www/html/html_date
verify
```bash
sudo find /var/www/html -type f | wc -l
sudo find /mnt/BlogBackups/Restore/html/ -type f | wc -l
```