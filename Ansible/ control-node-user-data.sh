#!/bin/sh 
# https://play.google.com/books/reader?id=B4o8NgAAAEAJ&pg=GBS.PA306.w.0.0.0.1_144
sudo useradd -m ansible_mgr
echo 'ansible_mgr ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers
sudo su - ansible_mgr << EOF
# ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
ssh-keygen -t ed25519 -C "ansible-homelab" -f ~/.ssh/id_ansible
sleep 120
ssh-keyscan -H web >> ~/.ssh/known_hosts
ssh-keyscan -H db >> ~/.ssh/known_hosts
# Installs the sshpass utility to allow for sending the ssh public key to the web and db VMs
sudo apt update -y && sudo apt install -y sshpass
echo "${admin_password}" | sshpass ssh-copy-id ansible_mgr@web
echo "${admin_password}" | sshpass ssh-copy-id ansible_mgr@db
EOF

# My part to manually copy the ssh key to the rpi_ups managed node
ssh-copy-id -i ~/.ssh/id_ansible.pub ansible_mgr@192.168.50.20