## Rocky linux prep
Create user for ansible
```bash
useradd -m -s /bin/bash ansible_mgr
passwd ansible_mgr

```
Add to sudoers
```bash
echo "ansible_mgr ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ansible_mgr
chmod 0440 /etc/sudoers.d/ansible_mgr
```
Enable password auth for time of SSH keys copy. Using Sed or via nano. 

```bash
sed -i 's/^#*PasswordAuthentication yes.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd
```
## Connect from ansible controler
Copy SSH key to remote. 
```bash
ssh-copy-id -i ~/.ssh/id_ansible.pub ansible_mgr@192.168.100.100
```
Test
```bash
ssh -i ~/.ssh/id_ansible ansible_mgr@192.168.100.100 "sudo whoami"
ssh -i ~/.ssh/id_ansible ansible_mgr@192.168.100.100 "whoami"
```

Disable password auth as now we have provisioned secure user. 

```bash
ssh -i ~/.ssh/id_ansible ansible_mgr@192.168.100.100 "sudo sed -i 's/^PasswordAuthentication yes.*/PasswordAuthentication no/' /etc/ssh/sshd_config && sudo rm -f /etc/ssh/sshd_config.d/*.conf"

ssh -i ~/.ssh/id_ansible ansible_mgr@192.168.100.100 "sudo systemctl restart sshd"
```
Test connection without kyes. Should be Permission Denied
```bash
ssh -o PubkeyAuthentication=no ansible_mgr@192.168.100.100
```
Test with key
```bash
ssh -i ~/.ssh/id_ansible ansible_mgr@192.168.100.100 "whoami"
```
