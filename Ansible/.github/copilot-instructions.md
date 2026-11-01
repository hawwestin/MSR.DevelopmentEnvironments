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
- Use Ansible Vault for sensitive data.
- Use SSH keys with passphrases for all access.
- Make backups of all critical data before any changes. Fetch them to a secure local location.

The user must manually authorize every deployment.
No autonomous infrastructure modifications are allowed.
Access to the production cluster is restricted to authorized personnel only with SSH keys and passphrases. All operations must be logged and auditable.