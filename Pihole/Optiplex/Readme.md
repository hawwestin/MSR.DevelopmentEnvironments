# Info
LXC instance using host network 
```
networks:
  static:
    ipv4_address: 192.168.50.15
```	
As a investigation process I installed Pihole with host Network to eliminate Docker network layer while looking for errors. 

```
networks:
  static:
    name: docker-static-eth0
    external: true
```

Instance name Pihole3

## Base Image
debian-12-turnkey-core_18.1-1_amd64.tar.gz


## DATA
Other information to be copied from working instances
- CNAME records 
- Local DNS records