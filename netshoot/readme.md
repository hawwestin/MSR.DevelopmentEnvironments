# Testing MacVLAN with `netshoot`

### 1. Run the `netshoot` container in the same `macvlan` network

```bash
docker run -it --rm \
  --network docker-static-bond0 \
  --ip 192.168.50.98 \
  nicolaka/netshoot
```

> Note: Make sure that the IP address `192.168.50.98` is not already in use in your LAN.



---

### 2. Perform tests inside the `netshoot` container

#### ✅ Check UDP DNS:
```bash
dig google.com @8.8.8.8
```

#### ❌ Check TCP DNS:
```bash
dig +tcp google.com @8.8.8.8
```

#### 📡 Check ports:
```bash
nc -vz 8.8.8.8 53
```

#### 🔁 Check the route:
```bash
traceroute 8.8.8.8
```

#### 📊 Check fragmentation and MTU:
```bash
ping -M do -s 1472 8.8.8.8
```

---

## What does this tell us?

| Result                     | Conclusion                                               |
| -------------------------- | -------------------------------------------------------- |
| ✅ UDP works, ❌ TCP doesn't | Problem with TCP routing in `macvlan`/`bond0`            |
| ❌ Both don't work          | Problem with Internet access from `macvlan`              |
| ✅ Both work                | The issue lies in Pi-hole configuration, not the network |

# Testing Host network with `netshoot`

Or use the host network:
```bash
docker run -it --rm --network host --cap-add=NET_ADMIN nicolaka/netshoot
```
Shows hosts and transfers in real time. 
```bash
iftop -i eth0
```
or
```bash
nethogs eth0
```
or
```bash
watch -n 1 'ss -tupn'
```

# Common active ports

| port | note      | commands                                           |
| ---- | --------- | -------------------------------------------------- |
| 2049 | NFS share | `tcpdump -i eth0 host 192.168.50.20 and port 2049` |
