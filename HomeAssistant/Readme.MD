# References

- https://technotim.com/posts/create-your-own-zigbee-hub/ 
- [TechnoTIM YT](https://youtu.be/8e4oaUHlMsE?si=vdDhORQablWR1Nu3)
- Official Z2M documentation
    - [Z2M Getting started guide](https://www.zigbee2mqtt.io/guide/getting-started/)
    - [Z2M Linux plain installation and configuration](https://www.zigbee2mqtt.io/guide/installation/01_linux.html#configuring) 
    - [Z2M Docker](https://www.zigbee2mqtt.io/guide/installation/02_docker.html)
    - [Z2M docker-compose](https://www.zigbee2mqtt.io/guide/installation/02_docker.html#docker-compose)
    - [General limitations that apply to all Zigbee implementations](https://www.zigbee2mqtt.io/guide/faq/#what-does-and-does-not-require-repairing-of-all-devices)
- Github
    - https://github.com/Koenkk/zigbee2mqtt 
    - https://github.com/eclipse-mosquitto/mosquitto
    - https://github.com/home-assistant/core 
- Home Assistant documentation
    - [Getting started](https://www.home-assistant.io/getting-started/)
- MQTT documentation
    - Official page https://mqtt.org/    
    - [Open Source MQTT Mosquitto](https://www.mosquitto.org/)
    - [Docker image](https://hub.docker.com/_/eclipse-mosquitto)
    - [mosquitto.conf man page](https://www.mosquitto.org/man/mosquitto-conf-5.html)
- Open Thrad Border router
    - Official docker documentation and config/env variables https://openthread.io/guides/border-router/build-docker 


# LXC approach     

WIP

## On Proxmox
Connect your USB antena for zgibee or thread

```bash
root@opti3050:~# ls -l /dev/serial/by-id/
total 0
lrwxrwxrwx 1 root root 13 Jan 23 19:17 usb-Itead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_V2_646c2ab588f3ef1RedactedRedactedR-if00-port0
```
This will return exact path you want to bind into the LXC.

No udev rule is needed because by-id is already stable.\
Udev rules are only needed when:
- a device does not appear under /dev/serial/by-id/
- or you want to rename it to something custom
If!? Your dongle is already exposing a stable ID, you're good.

## Add the Zigbee stick to the LXC config
Edit conf file of your LXC:
```bash
nano /etc/pve/lxc/108.conf
```
Add these two lines:
```conf
lxc.cgroup2.devices.allow: c 188:* rwm
lxc.mount.entry: /dev/serial/by-id/usb-Itead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_V2_646c2ab588f3ef11a24ac41b6d9880ab-if00-port0 dev/ttyUSB-Zigbee none bind,optional,create=file,uid=0,gid=20,mode=0660
lxc.mount.entry: /dev/serial/by-id/usb-SONOFF_SONOFF_Dongle_Plus_MG24_2a84c587a2a2ef11aRedactedRedacte-if00-port0 dev/ttyUSB-Thread none bind,optional,create=file,uid=0,gid=20,mode=0660
```
Restart the container
```bash
pct reboot 108
```

## Inside LXC
This gives you inside the container:
```bash
ls -l /dev/ttyUSB-Zigbee
ls -l /dev/ttyUSB-Thread
```
Why this is ideal:
- 188 is the major number for all ttyUSB devices (cgroup2 stuff)
- You avoid /dev/ttyUSB0 randomness
- You get a predictable name inside the container
- You avoid collisions if you add more USB serial devices later

### Fix the permissions inside the unprivileged LXC
In Proxmox Terminal 

```bash
chgrp 100020 /dev/ttyUSB0
chgrp 100020 /dev/ttyUSB1
```
check
```bash
root@opti3050:~# ls -l  /dev/ | grep USB
crw-rw----  1 root  100020 188,   0 Jul  4 17:04 ttyUSB0
crw-rw----  1 root  100020 188,   1 Jul  4 16:44 ttyUSB1
```
Then in LXC 
```bash
root@HomeAssistant ~# ls -l  /dev/ | grep USB
crw-rw---- 1 nobody dialout 188, 1 Jul  4 16:44 ttyUSB-Thread
crw-rw---- 1 nobody dialout 188, 0 Jul  4 17:10 ttyUSB-Zigbee
```