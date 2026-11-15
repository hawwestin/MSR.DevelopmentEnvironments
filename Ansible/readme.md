This project manages a educational homelab with Proxmox cluster.
We are using Ansible to orchestrate configuration and deployment of the cluster and its services.


# Trobleshooting 
If ansible keep stuck on tasks and next execution cannot even start. We may need to clean old sessions
```bash
pkill -f ansible || true
pkill -f ssh || true
```