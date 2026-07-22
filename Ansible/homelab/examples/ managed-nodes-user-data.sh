#!/bin/sh
# Modern DevOps Practices - Chapter 9 Setting up ansible 
# https://play.google.com/books/reader?id=B4o8NgAAAEAJ&pg=GBS.PA305.w.0.0.0.1_236
# This script sets up the Ansible managed nodes; user and configures passwordless SSH access to the managed nodes.
# Execute this script on the Vms that will be managed by Ansible (LXCs and VMs, and phisical machines).
# Admin password is passed in as a parameter to the script (if executed from terraform), and is used to set the password for the ansible_mgr user.
sudo useradd -m ansible_mgr
echo 'ansible_mgr ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers
sudo su - ansible_mgr << EOF
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
printf "${admin_password}\n${admin_password}" | sudo passwd ansible_mgr
EOF