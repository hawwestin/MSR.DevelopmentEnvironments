# CRITICAL INFRASTRUCTURE SAFETY RULES

This project manages a educational homelab with Proxmox cluster.
We are using Ansible to orchestrate configuration and deployment of the cluster and its services.
The following rules are mandatory for any Ansible playbook or task that interacts with the Proxmox cluster or its services. These rules are designed to prevent accidental disruption of the cluster, data loss, or other critical failures.

Generated code or configuration must be reviewed and approved by a human operator before execution. No autonomous or unsupervised operations are allowed on the production cluster.

Make it a habit to use `--check` and `--diff` options with Ansible commands to preview changes before applying them. Always verify the current state of the cluster and its services before making any modifications.

Code need to be easily understandable and maintainable. Include comments and documentation for any complex logic or operations. Avoid using hardcoded values; use variables and templates instead.

Main goal is an educational value dirving my homelab for myself and for others to learn from it. So make sure to document any changes, configurations, or procedures in the repository's README files or other appropriate documentation.

NEVER:
- Execute shutdown or reboot commands.
- Stop, restart or disable Proxmox services.
- Stop, migrate or modify running VMs or LXCs.
- Trigger NUT forced shutdown procedures.
- Execute poweroff, shutdown, reboot, halt commands.
- Modify cluster quorum or HA configuration without approval.

ALWAYS:
- Perform verification of current state over read-only operations.
- Generate code and configuration without executing them if no tested.
- Use Ansible --syntax-check before deployment.
- Use --check --diff where supported.
- Explain potentially destructive operations.
- Remind when backups are required
- Ask for explicit user approval before any infrastructure changes.
- Use Ansible Vault for sensitive data.
- Use SSH keys with passphrases for all access.
- Make backups of all critical data before any changes. Fetch them to a secure local location.

The user must manually authorize every deployment.
No autonomous infrastructure modifications are allowed.
Access to the production cluster is restricted to authorized personnel only with SSH keys and passphrases. 