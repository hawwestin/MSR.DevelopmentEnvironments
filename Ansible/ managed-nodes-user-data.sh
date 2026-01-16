#!/bin/sh
# https://play.google.com/books/reader?id=B4o8NgAAAEAJ&pg=GBS.PA305.w.0.0.0.1_236
sudo useradd -m ansible_mgr
echo 'ansible_mgr ALL=(ALL) NOPASSWD:ALL' | sudo tee -a /etc/sudoers
sudo su - ansible_mgr << EOF
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
printf "${admin_password}\n${admin_password}" | sudo passwd ansible_mgr
EOF