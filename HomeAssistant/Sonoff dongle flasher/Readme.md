# External info
https://hub.docker.com/r/ewelink/sonoff-dongle-flasher

Docker image for SONOFF Dongle Flasher — flash firmware for SONOFF Zigbee/Thread/Z-Wave dongles.

## devices
Those need to be provided based on your infrastrucutre. My short paths are made as I provide them to LXC container to those short paths. 

Check yours paths via: 
```bash
ls -l /dev/serial/by-id/
```

I run this along HomeAssistant within same LXC to upgrade my antenas. 