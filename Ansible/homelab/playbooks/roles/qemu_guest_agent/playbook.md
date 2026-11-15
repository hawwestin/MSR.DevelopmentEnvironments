documentation of playbooks in this directory. 
## QEMU guest agent on VMs

The `qemu_guest_agent` role supports Debian-family Linux with systemd and
pfSense on FreeBSD. On Debian it updates the apt cache, installs
`qemu-guest-agent`, and enables and starts its systemd service. The playbook
targets only `VM`, one host at a time. Other platforms are rejected.

Enable QEMU Guest Agent in **Proxmox VM > Options**, or run
`qm set <vmid> --agent enabled=1` on the Proxmox node. A scheduled full VM
stop/start may be necessary to expose the channel; a guest reboot alone may
not suffice. This playbook does not modify hypervisor settings, firewall
configuration, or network settings, and never reboots guests.

### Connection prerequisites

Debian guests must already have the automation account provisioned. The `VM`
group inherits the `ansible` SSH user and sudo from `???`.

For pfSense, enable SSH only from trusted management networks, configure key
authentication and root-capable access, and verify a compatible Python
interpreter is available **before** running this fact-gathering playbook.
Do not run the Linux bootstrap role on pfSense. Provisioning accounts or
installing Python is outside this role's scope.

Add the firewall to inventory yourself when ready. Override inherited settings
for that host as needed: `ansible_user`, `ansible_become`,
`ansible_become_method`, and `ansible_python_interpreter` (the actual installed
interpreter under `/usr/local/bin`). A root SSH connection needs
`ansible_become: false`; a non-root connection needs a working escalation
method. For a non-POSIX login shell, set `ansible_shell_type: sh` and
`ansible_shell_executable: /bin/sh`. No inventory changes are required until
the host and access are ready.

### pfSense package and startup behavior

The role verifies `/etc/platform`, root privileges, the release/ABI, and
`/dev/vtcon/org.qemu.guest_agent.0` before installing anything. It installs
only `qemu-guest-agent` from the existing repository named `pfSense`, using
its catalog and a dry-run transaction first. It refuses transactions that
upgrade, downgrade, reinstall, or remove existing packages. It never enables
generic FreeBSD repositories, bypasses ABI checks, or performs a global
package upgrade. If the package is unavailable, the role stops; another
package source requires separate review.

Availability on pfSense CE 2.9 is not guaranteed by this role and must be
verified on the actual build. Repository availability does not imply official
pfSense GUI-package support. See Netgate's
[add-on package warnings](https://docs.netgate.com/pfsense/en/latest/recipes/freebsd-pkg-repo.html).
Back up the firewall configuration and establish console access before deployment.

The role verifies the package's service interface, stores agent settings in
`/etc/rc.conf.local`, and leaves generated `/etc/rc.conf` and the vendor rc
script untouched. A guarded `/usr/local/etc/rc.d/ansible-qemu-guest-agent.sh`
hook starts the service at boot and tolerates repeated pfSense event calls
without starting duplicate processes. Settings changes restart only the agent.
These local files are outside normal pfSense configuration backups and may
need to be restored by rerunning the role after firmware upgrades. The role
does not modify `config.xml`.

### Run and verify

From the harness directory in Linux/WSL, load the environment and unlock the
SSH key as described above. Validate syntax and try one VM before the group:

```bash
export ANSIBLE_CONFIG=./ansible.cfg
ansible-galaxy collection install -r requirements.yml
ansible-playbook playbooks/install-qemu-guest-agent.yml --syntax-check
ansible-playbook playbooks/install-qemu-guest-agent.yml --list-hosts
ansible-playbook playbooks/install-qemu-guest-agent.yml --limit exampleVM 
```

If the configured YAML callback is unavailable, first run
`export ANSIBLE_STDOUT_CALLBACK=ansible.builtin.default`.
After verifying the trial VM, apply to the full `VM` group:

```bash
ansible-playbook playbooks/install-qemu-guest-agent.yml
```

On the guest, verify with `systemctl is-active qemu-guest-agent` and
`systemctl is-enabled qemu-guest-agent`. Repeating the playbook leaves an
installed package and running service unchanged, although refreshing the apt
cache can still report a change. Check mode on a fresh guest may fail at the
service task because it does not actually install the package.

For pfSense, deploy only to the firewall after adding its inventory entry:

```bash
ansible-playbook playbooks/install-qemu-guest-agent.yml --limit pfsense --check
ansible-playbook playbooks/install-qemu-guest-agent.yml --limit pfsense
```

Check mode does not refresh the pfSense catalog, install packages, restart
services, or create startup files. A fresh guest requires an existing catalog
to preview installation, and skips configuration/service checks until the
package is installed. It is not proof of successful deployment.

On pfSense, verify `pkg info qemu-guest-agent` and
`service qemu-guest-agent onestatus`. On its Proxmox node, verify
`qm agent <vmid> ping`. Run the limited playbook again and expect no unnecessary
package, configuration, or service changes. Repeat the startup hook with
`/usr/local/etc/rc.d/ansible-qemu-guest-agent.sh start` and confirm there is
still only one agent process. Schedule a user-approved reboot later and
repeat service and Proxmox ping checks to verify startup persistence. Do not
test shutdown or filesystem freeze on a live firewall.