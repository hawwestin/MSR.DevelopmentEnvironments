# !/bin/bash
# Backup NUT configuration files from remote server
ssh -t softpi@192.168.50.20 "sudo cat /etc/nut/ups.conf" > ./ups.conf
ssh -t softpi@192.168.50.20 "sudo cat /etc/nut/upsd.conf" > ./upsd.conf
ssh -t softpi@192.168.50.20 "sudo cat /etc/nut/upsd.users" > ./upsd.users

ssh -t softpi@192.168.50.20 "sudo tar -cz -C /etc/nut ." | tar -xz -C ./nut_backup/


scp root@192.168.50.5:/etc/nut/nut.conf ./nut.conf


ansible all -i 192.168.50.20, -u softpi --become -m fetch -a "src=/etc/nut/ups.conf dest=./backup/ flat=yes"