#!/usr/bin/env python3
"""
This script is a helper for Ansible users to enroll SSH host keys from an
inventory into the user's known_hosts file. It is intended for use with a
trusted inventory and a trusted console or administrator. It does not verify
the keys against a certificate authority or other external source. It is not
intended for use with untrusted hosts or inventories. It is not a replacement
for SSH host key verification, but a convenience for users who manage many
hosts and want to avoid interactive prompts for each new host! I know how annoying this is, 
and I want to help you avoid it. But please do not use this script to blindly trust unknown hosts!!!

In General:
Append verified SSH host keys from an Ansible inventory to known_hosts.

Run this script from the same Linux/WSL user and shell that you use for
Ansible. Start with a dry run to see which hosts and keys will be checked:

    python3 enroll-host-keys.py --dry-run
    python3 enroll-host-keys.py
    python3 enroll-host-keys.py --group new 
    python3 enroll-host-keys.py --group new --inventory ../path/to/other/inventory.ini

The script loads hosts with ``ansible-inventory --list``, then scans each
unique ``ansible_host`` and SSH port with ``ssh-keyscan``. It displays the
SHA256 fingerprints for the scanned keys. Before confirming a new host, compare
all displayed fingerprints with a trusted server console or administrator.
For example, on a server console, display its Ed25519 fingerprint with:

    ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub

Use the equivalent public-key file for RSA or ECDSA keys. The default group is
``new``; ``--group proxmox`` includes Proxmox nodes.

Use ``--inventory PATH`` to select another Ansible inventory, or
``--known-hosts PATH`` to select another known-hosts file (for example, when
testing). This helper supports direct SSH connections; it does not support
proxy/jump-host or host-key-alias settings.

Existing matching keys are skipped. Changed or additional keys for an
already-trusted endpoint are refused without changing its entries. Verify
legitimate key rotations and review them manually. Unrelated known-hosts
entries are preserved. A dry run never writes keys. Skipped confirmations and
failed hosts produce a nonzero exit status. Do not run multiple instances at
the same time against the same known-hosts file.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def inventory_targets(inventory_data, group_name):
    """Yield each unique SSH host and port in an inventory group.

    Child groups are included. Hosts configured for a non-SSH connection are
    skipped. Each yielded tuple contains the inventory host name, connection
    address, and SSH port.
    """
    host_variables_by_name = inventory_data.get('_meta', {}).get('hostvars', {})
    visited_group_names = set()
    inventory_host_names = set()

    def visit_group(current_group_name):
        """Add hosts from this group and recursively visit its child groups."""
        if current_group_name in visited_group_names:
            return
        visited_group_names.add(current_group_name)
        if current_group_name not in inventory_data:
            raise ValueError(f'Inventory group not found: {current_group_name}')
        group_data = inventory_data[current_group_name]
        inventory_host_names.update(group_data.get('hosts', []))
        for child_group_name in group_data.get('children', []):
            visit_group(child_group_name)

    visit_group(group_name)
    unique_ssh_endpoints = set()
    for inventory_host_name in sorted(inventory_host_names):
        host_variables = host_variables_by_name.get(inventory_host_name, {})
        if host_variables.get('ansible_connection', 'ssh') not in ('ssh', 'smart'):
            continue
        host_address = str(host_variables.get('ansible_host', inventory_host_name))
        ssh_port = int(
            host_variables.get('ansible_port', host_variables.get('ansible_ssh_port', 22))
        )
        if host_address.startswith('-') or any(character.isspace() for character in host_address):
            raise ValueError(f'Invalid SSH address for {inventory_host_name}')
        if not host_address or not 1 <= ssh_port <= 65535:
            raise ValueError(f'Invalid SSH endpoint for {inventory_host_name}')
        if (host_address, ssh_port) not in unique_ssh_endpoints:
            unique_ssh_endpoints.add((host_address, ssh_port))
            yield inventory_host_name, host_address, ssh_port


def key_pairs(known_hosts_text):
    """Return the unique key-type and public-key pairs in known-hosts text."""
    parsed_key_pairs = set()
    for entry_line in known_hosts_text.splitlines():
        entry_fields = entry_line.split()
        if entry_fields and not entry_fields[0].startswith('#'):
            if entry_fields[0].startswith('@'):
                raise ValueError('Marked known-host entries require manual review')
            if len(entry_fields) >= 3:
                parsed_key_pairs.add((entry_fields[1], entry_fields[2]))
    return parsed_key_pairs


def enroll(host_address, ssh_port, known_hosts_path, dry_run):
    """Scan, verify, and optionally add keys for one SSH endpoint.

    Existing matching keys are accepted without changes. New keys are printed
    for manual fingerprint verification and are written only after the user
    types the exact requested confirmation. In dry-run mode, keys are never
    written.

    Return True when the endpoint is already trusted, successfully added, or
    only previewed in dry-run mode. Return False when the user skips it.
    Raise ValueError when scanning fails or trusted keys have changed.
    """
    known_hosts_entry_name = (
        host_address if ssh_port == 22 else f'[{host_address}]:{ssh_port}'
    )
    key_scan_result = subprocess.run(
        ['ssh-keyscan', '-T', '5', '-p', str(ssh_port), host_address],
        capture_output=True, text=True, check=False,
    )
    scanned_key_entries = '\n'.join(sorted({
        entry_line for entry_line in key_scan_result.stdout.splitlines()
        if entry_line.strip() and not entry_line.startswith('#')
    })) + '\n'
    scanned_key_pairs = key_pairs(scanned_key_entries)
    if key_scan_result.returncode != 0 or not scanned_key_pairs:
        raise ValueError(f'No usable SSH scan for {known_hosts_entry_name}')

    existing_key_pairs = set()
    if known_hosts_path.exists():
        existing_key_scan = subprocess.run(
            [
                'ssh-keygen', '-F', known_hosts_entry_name,
                '-f', str(known_hosts_path),
            ],
            capture_output=True, text=True, check=False,
        )
        if existing_key_scan.returncode not in (0, 1):
            raise ValueError(f'Cannot read known hosts for {known_hosts_entry_name}')
        existing_key_pairs = key_pairs(existing_key_scan.stdout)
    if existing_key_pairs:
        if scanned_key_pairs <= existing_key_pairs:
            print(f'{known_hosts_entry_name}: already trusted')
            return True
        raise ValueError(
            f'{known_hosts_entry_name}: changed or additional keys; '
            'known_hosts left unchanged. Verify the change through a trusted '
            'console and review it manually.'
            # The user must manually remove the old keys from known_hosts and re-run this script to add the new keys.
            # ssh-keygen -R <host> -f <known_hosts_file>
        )

    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8') as fingerprint_input_file:
        fingerprint_input_file.write(scanned_key_entries)
        fingerprint_input_file.flush()
        subprocess.run(['ssh-keygen', '-lf', fingerprint_input_file.name], check=True)
    if dry_run:
        print(f'{known_hosts_entry_name}: new keys; dry run, not written')
        return True
    print('Compare ALL fingerprints above with a trusted console or administrator.')
    user_confirmation = input(
        f'Type "trust {known_hosts_entry_name}" to add these keys, or Enter to skip: '
    )
    if user_confirmation != f'trust {known_hosts_entry_name}':
        print(f'{known_hosts_entry_name}: skipped')
        return False
    known_hosts_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    known_hosts_file_descriptor = os.open(
        known_hosts_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600
    )
    with os.fdopen(known_hosts_file_descriptor, 'a', encoding='utf-8') as known_hosts_file:
        known_hosts_file.write('\n' + scanned_key_entries)
    print(f'{known_hosts_entry_name}: added')
    return True


def main():
    """Parse command-line options and enroll the selected inventory hosts."""
    argument_parser = argparse.ArgumentParser(
        description='Enroll verified SSH keys for a group in the Ansible inventory.'
    )
    argument_parser.add_argument(
        # Add new groups here as needed. The default group is "new" for hosts that are not yet trusted.
        '--group', choices=['proxmox', 'new'],
        default='new',
    )
    argument_parser.add_argument(
        '--inventory', type=Path,
        default=Path(__file__).resolve().parent / '..' / 'homelab' / 'inventory' / 'hosts.ini',
    )
    argument_parser.add_argument(
        '--known-hosts', type=Path,
        default=Path.home() / '.ssh' / 'known_hosts',
    )
    argument_parser.add_argument('--dry-run', action='store_true')

    parsed_arguments = argument_parser.parse_args()

    try:
        inventory_command_result = subprocess.run(
            [
                'ansible-inventory', '-i', str(parsed_arguments.inventory),
                '--list',
            ],
            capture_output=True, text=True, check=True,
        )
        if inventory_command_result.stderr:
            print(inventory_command_result.stderr, file=sys.stderr, end='')
        host_targets = list(
            inventory_targets(
                json.loads(inventory_command_result.stdout),
                parsed_arguments.group,
            )
        )
        if not host_targets:
            raise ValueError(f'No SSH hosts found in {parsed_arguments.group}!!!')
        
        all_hosts_succeeded = True
        for inventory_host_name, host_address, ssh_port in host_targets:
            print(f'\n{inventory_host_name} ({host_address}:{ssh_port})', flush=True)

            try:
                all_hosts_succeeded = enroll(
                    host_address,
                    ssh_port,
                    parsed_arguments.known_hosts.expanduser(),
                    parsed_arguments.dry_run,
                ) and all_hosts_succeeded
            except (OSError, ValueError, subprocess.CalledProcessError) as error:
                print(str(error), file=sys.stderr)
                all_hosts_succeeded = False

        return 0 if all_hosts_succeeded else 1
    
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Enrollment failed: {error}', file=sys.stderr)
        return 1
    
    except (EOFError, KeyboardInterrupt):
        print('\nEnrollment cancelled.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

# Im not python developer, so please forgive any mistakes. 
# I am just trying to help you avoid the pain of manually confirming SSH host keys for many hosts in an Ansible inventory.
# So if you find any bugs or have suggestions for improvements, please let me know. I will try to fix them as soon as possible. Thank you for using this script!