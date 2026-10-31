# CRITICAL INFRASTRUCTURE SAFETY RULES

This project manages a production Proxmox homelab
cluster using Ansible and NUT.

NEVER:
- Execute shutdown or reboot commands.
- Stop, restart or disable Proxmox services.
- Stop, migrate or modify running VMs or LXCs.
- Trigger NUT forced shutdown procedures.
- Execute poweroff, shutdown, reboot, halt commands.
- Run Ansible playbooks against production infrastructure.
- Modify cluster quorum or HA configuration without approval.

ALWAYS:
- Prefer read-only operations.
- Generate code and configuration without executing them.
- Use Ansible --syntax-check before deployment.
- Use --check --diff where supported.
- Explain potentially destructive operations.
- Ask for explicit user approval before any infrastructure changes.

The user must manually authorize every deployment.
No autonomous infrastructure modifications are allowed.