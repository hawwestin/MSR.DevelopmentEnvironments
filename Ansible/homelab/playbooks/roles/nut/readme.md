# General
Configuration of NUT Ups tools. Server and client roles.

Document and manually review Proxmox play commands; run them only by the user with the passphrase-protected SSH key loaded in `ssh-agent`.

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
- Proxmox Cluster HA management && Ceph converged cluster management
    - for upssched-cmd design and review Proxmox HA and Ceph shutdown coordination before enabling NUT monitor services or automatic shutdown behavior to keep homelab safe in case of power loss 
- Add appropriate monitor restart handling if and when `nut-monitor` is approved for activation.
- Wolnut > automate power on of the down proxmox cluster in case power is back online and UPS have enough Juice to power it back on and power off in case of another power loss. It require some time to start and to stop again host. 


## Role Configuration
The role renders `nut.conf`, `upsmon.conf`, `upssched.conf`, and `upssched-cmd` on server and client hosts. The server additionally receives `ups.conf`, `upsd.conf`, and `upsd.users`. Passwords used by these templates belong in the inventory Ansible Vault file at `inventories/group_vars/all/vault.yml`; do not commit plaintext credentials.

Required Vault variables are `vault_nut_monitor_password`, `vault_nut_admin_password`, and `vault_nut_qnap_admin_password`. The QNAP `[admin]` compatibility account is retained, but its password is supplied through Vault.

The role always stops and disables `nut-monitor`. Do not enable it until the Proxmox HA and Ceph shutdown coordination described above has been designed, tested safely, and explicitly approved. Proxmox/cluster playbooks are user-run only; an AI agent must not execute them.

The read-only preflight run on 2026-11-02 found `nut-monitor` active and enabled on `pve2` and `opti3050` (inactive and disabled on `opti3040`). These PVE monitors are secondary clients with power value 1 and `MINSUPPLIES 1`; NUT's native critical-battery path can invoke `SHUTDOWNCMD` independently of the callback. Do not induce a UPS event or enable further automatic behavior until the user has reviewed and stopped the active monitor services. This is a point-in-time observation; verify service state again before any test or deployment.

`LOWBATT` is routed to the callback. Its gate requires `OB` status, valid integer runtime and load readings, and either runtime below the configured safe threshold or load at/above the configured limit. Missing or malformed readings fail closed. Both `LOWBATT` and `SHUTDOWN` currently log a met gate without requesting FSD; the coordinated shutdown action is not implemented yet.

## Log-Only Callback Test

`nut_test_mode` defaults to `false`. From the repository root, review the safe test configuration on `opti3040` with:

```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit opti3040 --check --diff -e nut_test_mode=true
```

Only the user may run a deployment, after reviewing the diff. To deploy the test configuration, run the same command without `--check`:

```bash
ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit opti3040 --diff -e nut_test_mode=true
```

Test mode leaves `nut-monitor` stopped and disabled, sets the monitored power value to zero, uses a logger-only `SHUTDOWNCMD`, routes scheduler timers through isolated runtime files, and makes the callback write to syslog and `wall` without invoking `upsmon -c fsd`.

With test mode deployed, run callback cases directly on `opti3040` to exercise the LOWBATT gate without changing UPS state:

```bash
sudo env UPSNAME=CBSups NOTIFYTYPE=LOWBATT NUT_TEST_UPS_STATUS=OB NUT_TEST_BATTERY_RUNTIME=400 NUT_TEST_UPS_LOAD=80 /etc/nut/upssched-cmd lowbatt
sudo env UPSNAME=CBSups NOTIFYTYPE=LOWBATT NUT_TEST_UPS_STATUS=OB NUT_TEST_BATTERY_RUNTIME=200 NUT_TEST_UPS_LOAD=40 /etc/nut/upssched-cmd lowbatt
sudo env UPSNAME=CBSups NOTIFYTYPE=LOWBATT NUT_TEST_UPS_STATUS=OL NUT_TEST_BATTERY_RUNTIME=200 NUT_TEST_UPS_LOAD=80 /etc/nut/upssched-cmd lowbatt
sudo env UPSNAME=CBSups NOTIFYTYPE=LOWBATT NUT_TEST_UPS_STATUS=OB NUT_TEST_BATTERY_RUNTIME=invalid NUT_TEST_UPS_LOAD=80 /etc/nut/upssched-cmd lowbatt
sudo env UPSNAME=CBSups NOTIFYTYPE=SHUTDOWN NUT_TEST_UPS_STATUS=OB NUT_TEST_BATTERY_RUNTIME=200 NUT_TEST_UPS_LOAD=40 /etc/nut/upssched-cmd shutdowncritical
```
Test results
```bash
sudo journalctl -t upssched-cmd --since "5 minutes ago"
```

To exercise scheduler routing, while test mode is deployed and `nut-monitor` remains stopped:

```bash
sudo env UPSNAME=CBSups NOTIFYTYPE=SHUTDOWN NUT_TEST_UPS_STATUS=OB NUT_TEST_BATTERY_RUNTIME=200 NUT_TEST_UPS_LOAD=80 /usr/sbin/upssched
sudo env UPSNAME=CBSups NOTIFYTYPE=ONBATT /usr/sbin/upssched
sudo env UPSNAME=CBSups NOTIFYTYPE=ONLINE /usr/sbin/upssched
```

`ONBATT` starts a five-second test timer; `ONLINE` cancels it. You can also omit the `ONLINE` invocation and observe the timer callback. These are synthetic scheduler events only; do not generate a real UPS power-loss or shutdown event. After testing, restore the normal rendered configuration by running the playbook without `-e nut_test_mode=true`, again limited to `opti3040` and user-run only.

For a Proxmox check-mode review, start `ssh-agent`, add the passphrase-protected key, then run this from the repository root:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_windows

export ANSIBLE_CONFIG="$PWD/Ansible/homelab/ansible.cfg"
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault-password

ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit opti3040 --check --diff

ansible-playbook -i Ansible/homelab/inventories/hosts.ini Ansible/homelab/playbooks/nut.yml --limit proxmox --check --diff
```
Only run a non-check deployment after reviewing the diff and explicitly authorizing it.
