# General
References to official documentation
- https://apps.heimdall.site/
- https://hub.docker.com/r/linuxserver/heimdall
- https://docs.linuxserver.io/images/docker-heimdall
- https://github.com/linuxserver/docker-heimdall/pkgs/container/heimdall
- https://github.com/linuxserver/Heimdall
- TechnoTim installation guide https://youtu.be/PA01Z6-z8Qs

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
This config is prepared to be accesed through reverese proxy and be configured there over hostname of running container. Thats why it does not expose any ports. 
In case you run it without NginxProxyManager please add port 80 and 443 as exposed. 
```
    ports:
      - 80:80
      - 443:443
```
### Enhanced apps

Connection must be checked if works with test option,
Verify browser console to check issues with connection to apps.\
Known issues: 
- PHP in backend hates SSL mismatch so for enhanced api calls try to use HTTP instead of DNS with HTTPS. Or provide maching and valid SSL with domain of connected service to heimdall.

## Mash multi node dashboards 

In Mesh configuration we use remote mounted data for container so all Heimdalls use the same local data and are always in sync. 

Example of network creation connected directly to QANP ethernet port number one or two. That allow to host Heimdall with dedicated IP addrress 

### Requirements
1.  create on NFS host network resource
2.  test connection on local container via mount over 127.0.0.1
3.  all meshed heimdalls must use the same UserID and GroupID in all nodes

### Direct connection from Docker on NFS.
NOT reccomeded, translate arguments and examples.

### Create directory for config files. 
On your NAS or Storage server creat new NFS share. Configure it to be accesed for specific IP or ranege of your homelab network. 
- 👉verivy squash permission that was set. 

### Connect to NFS share 
If you wanna share configuration or have heimdalls accessible over few instances use NFS/CISF share to have one source of configs. 
```
mkdir -p /mnt/{{remoteHostname}}/heimdall/config
```
