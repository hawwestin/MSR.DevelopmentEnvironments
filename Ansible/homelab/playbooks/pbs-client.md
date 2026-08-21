# Raspberry Pi PBS client

This playbook installs the Proxmox Backup Client on the `raspberrypi` physical-host group and schedules a daily backup of:

- `/etc`
- `/opt`
- `/docker`
- `/var/lib/docker/volumes`

The backup is a file archive for recovery onto a fresh Debian/Raspberry Pi OS installation. It is not a bootable disk image. Docker databases may need application-specific exports for consistent recovery.

## PBS preparation

Create a dedicated PBS user and API token. Grant the token the `DatastoreBackup` role on `/datastore/QnapLocal`. Use the PBS datastore connection information to obtain the server TLS fingerprint.

Store the token secret in an encrypted group variable file. For example, create `inventories/group_vars/raspberrypi/vault.yml` with:

```yaml
pbs_api_token_secret: replace-with-the-token-secret
```

Then encrypt it with the repository's normal Ansible Vault workflow:

```bash
ansible-vault encrypt inventories/group_vars/raspberrypi/vault.yml \
  --vault-password-file ~/.ansible/vault-password
```

Set the fingerprint in `inventories/group_vars/raspberrypi.yml` before applying the playbook.

## Run

Run from the repository root and select the physical-host inventory explicitly:

```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password
ANSIBLE_CONFIG=Ansible/homelab/ansible.cfg \
ansible-playbook \
  -i Ansible/homelab/inventories/hosts.ini \
  Ansible/homelab/playbooks/pbs-client.yml \
  --limit rpi_ups
```

The target must use 64-bit Debian-family Linux and a supported Debian release. The playbook manages `/etc/apt/sources.list.d/pbs-client.sources`; it does not modify the existing `sources.list`.

## Verify

```bash
ssh rpi_ups systemctl status proxmox-backup-client.timer
ssh rpi_ups journalctl -u proxmox-backup-client.service
```

Run a controlled backup with:

```bash
ssh rpi_ups sudo systemctl start proxmox-backup-client.service
```

Check the `QnapLocal` datastore and the `raspberrypi` namespace in PBS. Test restoring a small file set before relying on the backup during recovery.
