# General
References to official documentation
- https://apps.heimdall.site/
- https://hub.docker.com/r/linuxserver/heimdall
- https://docs.linuxserver.io/images/docker-heimdall
- https://github.com/linuxserver/docker-heimdall/pkgs/container/heimdall
- https://github.com/linuxserver/Heimdall
- TechnoTim installation guide https://youtu.be/PA01Z6-z8Qs

# First installation
## Prepare new host for container
### User for file ownership

References to linux user management articles. 
- [How to Create Users in Linux (useradd Command)](https://linuxize.com/post/how-to-create-users-in-linux-using-the-useradd-command/)
- [How to List Groups in Linux](https://linuxize.com/post/how-to-list-groups-in-linux/)
- [How to List Users in Linux](https://linuxize.com/post/how-to-list-users-in-linux/)
- [How to Add and Remove Users on Ubuntu 20.04](https://linuxize.com/post/how-to-add-and-delete-users-on-ubuntu-20-04/)

List all users:
```
cut -d: -f1 /etc/passwd
```
In case of existing docker user or mistakes delete user and recreate it. 
```
deluser username
```
Add existing user to group
```
usermod -a -G groupname username
```
Checklist
1. Create user for docker compose
	- UserName Heimdall <- or any custom name>
	- userId 1005 <- randomly chosen first free id. Please rememeber that for mesh it need to be the same on all hosts>
	- PGID 100 <- Group default users on linux is by default 100> 		
2. It is required to add new user to 'docker' group?
	1. no

Adding of new user with provided default group, id and name
```
useradd -g users -u 1005 heimdall
```
Where -g is the basic group
Test of created user 
```
id heimdall 
```
👉This user and group id now can be provided in docker-compose.yml file. 

## Simple local configuration

Basic configuration can be found at docker-compose.yml
This config is prepared to be accesed through reverese proxy and be configured there over hostname of running container. Thats why it does not expose any ports. \
In case you run it without NginxProxyManager please add port 80 and 443 as exposed. Also you can remove nginx external network and allow docker to create and use default one. \
Snippet for ports: 
```
    ports:
      - 80:80
      - 443:443
```

# Mash multi node  
If you wanna share configuration or have heimdalls accessible over few instances use NFS/CISF share to have one source of configs. 

In Mesh configuration we use remote mounted data for container so all Heimdalls use the same not local data and which are always in sync. 

Drowback of such solution is that we break single responsibility principle. And now those host depend on our NAS/data host. In case of it is not accessible your heimdall will display not configured dashboard. When conectivity to NFS share is back online you have to restart container. This hovewer can be automated. 

**Disclaimer!** \
Below examples were tested with NAS of `QNAP` brand and example snippets may contain unique to my homelab names or settings. 

Resources 
- [ Don't use local Docker Volumes - YT](https://youtu.be/eKAQiYu4NyI)

## NFS Share checklist
1. Create on host that will provide network resource new NFS share and apply security.
2. Test connection from host that will connect to that network share. 
3. Add to system Mount list this to be remounted on host startup. 
4. Use Path to mounted directory in docker-compose of services

### 1. Create NFS Share
On your NAS or Storage server creat new NFS share. Configure security to share to be accesed for specific IP or ranege of your homelab network. \
Create or check id of local user ID and group that will be an owner of this NFS share. 
On NFS Share options enable check of user access right. Thats why it is necesary to create on Heimdall host user with the same UserID and group so you can connect to One NFS Share and synchronize data from multiple nodes. Verify secure squash permission of root user that was set. 

Additional resources 
- [Basic NFS Security – NFS, no_root_squash and SUID](https://www.thegeekdiary.com/basic-nfs-security-nfs-no_root_squash-and-suid/)


### 2. Connect to NFS share 
SSH on Hiemdall host. First step is to create path that will be used as link to remote resources. Where `{{remoteHostname}}` is your NFS share host. In my examples it is `qnap`.
```
mkdir -p /mnt/{{remoteHostname}}/heimdall/config
```
Then we will test mount this new file to Remote share. Please be advice that case of letters in paths must match. Provide your NFS share hsot IP and path. Remember that it is case sensitive.
```
mount -t nfs -o vers=4,rw,bg,timeo=14 192.168.0.2:/nfs-volumes/heimdall_config/www /mnt/qnap/heimdall_config
```
Connection can de reset with `mount -av`. 
If connection works. Verify also that file permissions are also set to user id and group id of our Heimdall user.\
Try to create some file `touch test.txt` and verify permissions set on NFS share host. 

Code snippet for debugging options
```
docker service create -d \ 
    --name nfs-service \ 
    --mount 'type=volume,source=nfsvolume,target=/app,volume-driver=local,volume-opt=type=nfs,volume-opt=device=:/nfs-volumes,"volume-opt=o=addr=10.0.0.10,rw,nfsvers=4,async"' \ 
    nginx:latest
```

Additional resources
- [Common NFS mount options in Linux](https://www.thegeekdiary.com/common-nfs-mount-options-in-linux/)
### 3. Mount on host boot
To make this mount accessible on host start-up we have to add it to FStab.
Open in your favorite text editor file `/etc/FStab` and add sth similar as below.
```
192.168.0.2:/nfs-volumes/heimdall_config/www /mnt/qnap/heimdall_config nfs vers=4,rw,bg,timeo=14 0 0
```
Now for testing if it is working or if you done this first time please restart machine that connect to remote NFS Share. After restart verify that `mount -lv` list added resources as connected. If not you have to diagnose why it is not available, starting from journal logs. 

## 4. Add volume on mounted path.
As not all data should be synced between nodes we have to investigate which one should be unique per node and which directories we can share. In case of heimdall shared resources are in `/conifg/www` directory.\
If you have some date on old volume you can move them attaching both volumes to some shell container and in interactive mode copy files to new directory. This should be done on different container than service as service should not be running during such file operations. 
1. If you are using portainer you can create new volume on mounted path. Then you can attach this volume to container. For more examples refer to  [ Don't use local Docker Volumes - YT](https://youtu.be/eKAQiYu4NyI).
2. Or manually in docker-compose.yml you can use path to `/mnt/{{remoteHostname}}/heimdall/config:/config/www/`. 
At the end it should look like that with manually provided path. 
```
    volumes:       
      - config:/config
      - /mnt/qnap/heimdall_config:/config/www
```

After data are moved to new volume start container (or portainer stack). It should load data from mounted nfs share. Now when you change sth on one Heimdall changes will be visible on all nodes. 


## Direct connection from Docker on NFS.
NOT reccomeded! In case of lost connection to NFS host docker engine will retry to connect NFS share hard mounted in docker-compose you can lose controle over it as it will not respond to any commands. In such situations you could be forced to kill docker daemon with all other helthy services :/
Even when NFS service is back online it can still be unresponsive. If you use portainer agents to controle such node you will lose controle over it and will be forced to SSH to it and manually restart docker daemon. 

It is a valid solution for systems like QNAP or OpenMediaVoult, TrueNas which do not have easily available terminal to configure volumes/ mounts or FStab. In such situation you can provide complete NFS connection inside docker-compose.

Still If you want to try it here you have snippets for local available NFS share. IP can be changed to point to remote NFS Share. 
```
volumes: 
  nfs_config: 
    driver: local 
    driver_opts: 
      type: nfs 
      o: addr=127.0.0.1,rw,noatime,rsize=8192,wsize=8192,tcp,timeo=14,nfsvers=4  
      device: ":/nfs-volumes/heimdall_config/www" 
```

# App usage
Default configuration use on first dashboard admin account without passwords set. If you plan to use it for more people I can advice to create more users instead of using only admin account. Users can be treated like scoping instead of human beaings. For example for address using DNS and IP addresses.
Basic usage allow to add cards to any addres you provide. 

By default it also provide search input similar to browser welcome page. It can be changed, default is DuckDuckGo. 

You can also host your own search engine. More information how to do that can be found on Networkchuck YT channel. 

To aggregate cards you can create tags. Moving of cards between tags or default board is done on edit page or on rearange toolkit that can be enabled on board. There you can pin or unpin more than one at once. Tags card could also have customized colour.  

Other personalization options:
1. you can change default backgroud. I can advice to use sth light weight or use cache on nginxproxymanager or other solution. 
2. Customization of user account avatar. 
3. Application icon and colour of the card can be changed.

## Enhanced apps

Connection must be checked if works with `test` option,
Verify browser console to check issues with connection to apps.\
Known issues: 
- PHP in backend hates SSL mismatch so for enhanced api calls you must be sure that you provide maching and valid SSL with domain of connected service to heimdall. If you cannot obtain walid certificate try to use HTTP instead of DNS with HTTPS


# Other tested feature of docker
probably this will be moved to dedicated readme file or other documentation. 

As your device can have a few ethernet ports we can chose which one your contianers should use with network connected directly to ethernet port number one or two. That allow to host Heimdall with dedicated IP addrress. 

## Network creator from terminal
Name of ipam-driver network card need to be verified for your host. 
### DHCP mode
Create a new network named `qnet-dhcp-eth0`

```
docker network create -d qnet --ipam-driver=qnet --ipam-opt=iface=eth0 qnet-dhcp-eth0
```

### Static mode
Create a new network named `qnet-static-eth0`  
```
docker network create -d qnet --ipam-driver=qnet --ipam-opt=iface=eth0 --subnet=192.168.50.0/24 --gateway=192.168.50.1 qnet-static-eth0
```
To have naming standard and ease of moving containers we can recreate networks to sth like: 
```
docker network create -d qnet --opt=iface=eth1 --ipam-driver=qnet --ipam-opt=iface=eth1 --subnet=192.168.50.0/24 --gateway=192.168.50.1 docker-static-eth1 
```

Test Created networks to appear on list
```
docker network ls
```
Docker Run example DHCP
```
docker run --rm -it --net=qnet-dhcp-eth0 alpine ifconfig eth0
```
Docker Run example Static
```
docker run --rm -it --net=qnet-static-eth0 --ip=192.168.80.119 alpine ifconfig eth0
```

Network creator from docker compose
```
version: '2' 
services: 
  qnet_static: 
    image: alpine 
    command: ifconfig eth0 
    networks: 
      docker-static-eth1: 
        ipv4_address: 192.168.50.20 
networks: 
  docker-static-eth1:     
    driver: qnet 
    driver_opts: 
      iface: "eth1" 
    ipam: 
      driver: qnet 
      options: 
        iface: "eth1" 
      config: 
        - subnet: 192.168.50.0/24 
          gateway: 192.168.50.1
```
Then in services docker-compose add manually static ip address. 
```
    networks: 
      qnet-static: 
        ipv4_address: 192.168.50.9
```
And for other stacks you can connect with below changing eth0 and eth1 chosing with of endpoints should be used. 
```
networks: 
  qnet-static: 
    external: 
        name: qnet-static-eth0
```