# Set up Ansible on WSL

This guide walks through preparing Windows Subsystem for Linux (WSL) as an
Ansible control node. The control node is the computer where you run Ansible
commands; it connects to the Linux hosts you want to manage.

> **About names in this guide:** Names such as `id_ed25519_windows`,
> `REMOTE_USER`, and `REMOTE_HOST` are examples chosen for this guide. They are
> not official WSL or Ansible names. Replace example values with the names and
> addresses that apply to your setup.

## 1. Check your WSL version

Open PowerShell or Command Prompt and run:

```powershell
wsl --version
```

Mirrored networking, used in the optional VPN section, requires WSL version
`2.0.0` or later and a supported Windows 11 installation. If your WSL version
is older, or `wsl --version` is not recognized, update WSL before using that
feature. You can skip the update and VPN section if you do not need mirrored
networking and WSL is otherwise working.

## 2. Update WSL

Open PowerShell as an administrator and run:

```powershell
wsl --update
```

When the update finishes, restart WSL so the update takes effect:

```powershell
wsl --shutdown
```

This stops all running WSL distributions. Open your Linux distribution again
from the Start menu or run `wsl` in a terminal.

## 3. Optional: configure WSL networking for a VPN

Try this only if you have network or DNS problems while connected to a VPN.
Mirrored networking is available on supported Windows 11 installations.

1. In Windows Explorer, press **Windows + R**, enter `%USERPROFILE%`, and press
   **Enter**.
2. In that folder, open `.wslconfig`. If it does not exist, create a text file
   with that exact name (make sure it does not end in `.txt`).
3. Add these settings:

   ```ini
   [wsl2]
   networkingMode=mirrored
   dnsTunneling=true
   ```

4. Save the file, then run this in PowerShell or Command Prompt:

   ```powershell
   wsl --shutdown
   ```

Start your Linux distribution again to use the new settings.

## 4. Install Ansible in your Linux distribution

Open your WSL Linux terminal. These commands are for Ubuntu or Debian:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-full pipx sshpass
```

Install Ansible and Ansible Lint with `pipx`:

```bash
pipx install --include-deps ansible
pipx install ansible-lint
pipx ensurepath
```

Close and reopen the WSL terminal so the updated `PATH` is loaded. Then check
that the commands are available:

```bash
command -v ansible
ansible --version

command -v ansible-lint
ansible-lint --version

pipx list
```

The paths and Python versions shown by these commands depend on your Linux
username and installed software; your output will not necessarily match
someone else's.

### Update Ansible later

Update the two applications individually:

```bash
pipx upgrade ansible
pipx upgrade ansible-lint
```

To update all applications installed with `pipx`, run:

```bash
pipx upgrade-all
```

## 5. Optional: use an SSH key stored in Windows

This copies an existing SSH key from your Windows profile into WSL. Only do
this if you want to use that key from WSL. An SSH private key is secret: do not
share it or commit it to a repository.

Set `WINDOWS_USER` to your Windows account folder name. The source key below,
`id_ed25519`, is an example; change it if your key has a different filename.
The destination name, `id_ed25519_windows`, is also an example name you choose
for the copy.

```bash
WINDOWS_USER="replace-with-your-windows-user"
mkdir -p ~/.ssh

cp "/mnt/c/Users/$WINDOWS_USER/.ssh/id_ed25519" ~/.ssh/id_ed25519_windows
cp "/mnt/c/Users/$WINDOWS_USER/.ssh/id_ed25519.pub" ~/.ssh/id_ed25519_windows.pub

chmod 600 ~/.ssh/id_ed25519_windows
chmod 644 ~/.ssh/id_ed25519_windows.pub
ls -la ~/.ssh
```

Replace `replace-with-your-windows-user` with the folder name under
`C:\Users`. For example, if that folder is `sam`, set
`WINDOWS_USER="sam"`. If the source key has another name, use that name in both
`cp` commands.

## 6. Optional: copy your public key to a Linux host

`ssh-copy-id` adds your **public** key to a Linux host so you can sign in
without entering your account password each time. Replace the example account
and address below with the account and address for your host.

First, preview what would happen with `-n` (dry run):

```bash
REMOTE_USER="replace-with-linux-user"
REMOTE_HOST="192.0.2.10"

ssh-copy-id -n -i ~/.ssh/id_ed25519_windows.pub "$REMOTE_USER@$REMOTE_HOST"
```

The example address `192.0.2.10` is reserved for documentation; it is not a
real server address. Once you have checked the command and replaced both
example values, run it without `-n` to add the key:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_windows.pub "$REMOTE_USER@$REMOTE_HOST"
```
