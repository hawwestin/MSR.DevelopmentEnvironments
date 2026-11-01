# General
Configuration of NUT Ups tools. Server and client roles.

# Homelab context
UPS is connected via USB to Rasppbery Pi. Other hosts like proxmox and Qnap Nas are clients to it. 
Proxmox configuration is as code driven by this ansible playbook. 
Qnap Nas have a hardcoded configuration in /etc/nut that are locked to change. So to connect UPS via Rasppbery we had to emulate those options as a proxy ups and re-create hardcoded crudentials for Qnap. 

Proxmox Cluster (3 nodes) have enable High Availability. Some lxc containers will be migrated in event of one box is down. Nut logic must handle this in case of power loss and disarm HA before we start of controled shutdown. Without it LXC can start migration in the middle of shutdown of all hosts. 

Ceph converged cluster on proxmox nodes also need a dedicated logic to perform controled shutdown 

Access to all hosts are via SSH-Keys with passphrase. It is a safety standard that always should be fallowed. Therefor only You can apply those playbook. In today era of AI it is must have to prevent agents from roaming on your homelab without your intent applying half baked playbooks and reconfiguring things that may not be protected by backup. 

# UPS and power usage
Today I measure power usage via smart plug on the wall before UPS. This gives me overall context about power usage in Office. Seecondary data stream are collected directly from UPS. All data are saved to Home Assistant so I have long term data. Home assistant also leave on proxmox cluster. 

# ideas
NUT can do more automations in the future. Today I just don't want to damage any host and its data. 

# TODO
- Proxmox Cluster HA management
- Ceph converged clsuter management
