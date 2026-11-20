This project manages a educational homelab with Proxmox cluster.
We are using Ansible to orchestrate configuration and deployment of the cluster and its services.


# Trobleshooting 
If ansible keep stuck on tasks and next execution cannot even start. We may need to clean old sessions
```bash
pkill -f ansible || true
pkill -f ssh || true
```

# SSH manual snippets
## create new key
```bash
ssh-keygen -t ed25519 -C "ansible-homelab" -f ~/.ssh/id_ansible
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ansible
chmod 644 ~/.ssh/id_ansible.pub
```

## fetch to known hosts
```bash
ssh-keyscan -H 192.168.100.14 >> ~/.ssh/known_hosts
ssh-keyscan -p 2222 -H 192.168.50.1 >> ~/.ssh/known_hosts
```
## send keys
```bash
ssh-copy-id -i ~/.ssh/id_ansible.pub ansible_mgr@192.168.100.100
ssh-copy-id -i ~/.ssh/id_rsa_windows.pub root@192.168.50.6
```

## load ssh key for ansible
```bash
eval "$(ssh-agent -s)"
ssh-add "~/.ssh/id_ansible"
ssh-add -l
```