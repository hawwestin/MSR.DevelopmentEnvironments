# Create a user (without a GUI login password)
pveum user add ansible@pve -comment "Konto serwisowe dla Ansible"

# Grant read permissions across the entire cluster (required for the plugin to retrieve facts)
pveum acl modify / -user ansible@pve -role PVEAuditor

# Grant permissions to manage and create VMs/LXCs
pveum acl modify /vms -user ansible@pve -role PVEVMAdmin

# Grant permissions to use storage (creating disks for new LXCs)
pveum acl modify /storage -user ansible@pve -role PVEDatastoreAdmin

# Create an API token for the user (this is more secure than using a password)
pveum user token add ansible@pve token-ansible --privsep 0
# Add the generated token secret to your .env file for Ansible to use