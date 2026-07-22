# idea
I plan to connect Philips PureProtect Pro 4200 Series AC4220/12 to self hosted Home Assistant.
Now I have a stack HA MqTT and Z2M 
It live in vlan 100. Wifi is for IOT is in Vlan 10 in separate Lan. So traffic need to be passed over PFSense firewall rules. This I can handle with ease. 
In home assistant I need information what to add to connect to Air Purifier. I have philips App on mobile to monitor those current readings . Home assisnat for now will be more as a long term database. Later I will add some automations but now I have only few IOT gizmos

# things suggested By AI 
 Use the local CoAP integration (philips_airpurifier_coap / philips-air-purifier) or the philips-airctrl / aioairctrl CLI/library to talk to the AC4220 over encrypted CoAP (UDP port 5683). Make the purifier reachable from Home Assistant (allow UDP 5683 and mDNS if you want discovery), install the integration (HACS or manual custom_components) and point it at the purifier IP; you can also run a small poller to publish readings to MQTT if you prefer long-term storage. 

 What Home Assistant needs

- Integration options

    - philips_airpurifier_coap (local push integration / custom component). Installs via HACS or manual custom_components; HA will attempt autodiscovery or you can add by IP. Creates sensors for PM2.5/PM10, VOC, filter life, fan speed, modes, power, etc. 

    - philips-air-purifier / philips-airctrl / aioairctrl libraries and CLI - useful to discover, test and poll the device from a separate container or script; can be used to push data into MQTT for HA to consume. aioairctrl documents the CoAP endpoint and CLI usage. 

- Network / firewall requirements (actionable)

    - Allow UDP port 5683 (CoAP) from your HA host (VLAN 100) to the purifier (VLAN 10). This is the main protocol/port used. 

    - Allow UDP 5353 (mDNS) if you want automatic discovery across VLANs (or just add the purifier IP manually). 

    - Prefer a DHCP reservation or static IP for the purifier so the integration keeps a stable address.

    - If you run a separate poller/container that publishes to MQTT, allow that container to reach both the purifier and your MQTT broker.

Step-by-step (quick)

1.Find purifier IP (router DHCP table or Philips app).

1. Open firewall: permit UDP 5683 from HA to purifier; permit UDP 5353 if using discovery.

2. Install integration: via HACS add Philips AirPurifier (CoAP) or copy custom_components into HA. Restart HA. 

3. Add integration: Configuration > Devices & Services > Add Integration > Philips Air Purifier > enter IP (if not auto-discovered). 

4. Verify entities and check HA logs for CoAP debug if needed. Use philips-airctrl/aioairctrl to test reads from the purifier directly. 

Important caveats & troubleshooting

 - Stability warning: many community integrations rely on reverse‑engineered encrypted CoAP and can be unstable; devices sometimes stop responding and may require a power cycle or HA restart. Expect occasional reconnection issues.  https://github.com/kongo09/philips-airpurifier-coap?tab=readme-ov-file&utm_source=copilot.com

 - If you prefer maximum reliability, consider running a small poller (using aioairctrl/philips-airctrl) that publishes to MQTT; HA then reads from MQTT (good for long‑term DB and decoupling). https://pypi.org/project/aioairctrl/?utm_source=copilot.com

 and and and  .... nope 

 -------

 you’re in the perfect position to run the MQTT bridge container. This is actually the most stable long‑term architecture for Philips purifiers because it decouples HA from the sometimes‑flaky CoAP session handling.

Below is a complete, production‑ready workflow tailored to your VLAN‑segmented home‑lab and your HA + MQTT stack.

# Architecture overview (MQTT bridge)

Your setup will look like this:
```
Philips AC4220  <--CoAP UDP/5683-->  aioairctrl container  <--MQTT-->  Mosquitto  <--native-->  Home Assistant
```
 - The container polls the purifier every X seconds

 - Publishes readings to MQTT topics like:
 - philips/AC4220/state/pm25, .../voc, .../filter_life, .../mode, etc.

 - HA auto-discovers via MQTT Discovery or you define sensors manually.

This avoids HA talking CoAP directly and gives you buffering, retries, and stability.
## The Python tool you want: aioairctrl

This is the most mature library for Philips CoAP devices.
It supports:

    Encrypted CoAP (AES‑CBC)

    Status polling

    Control commands (power, fan speed, mode)

    JSON output

    Easy integration with MQTT

You’ll run it as a small service inside your HA docker‑compose stack.
### Docker Compose service (ready to drop in)
Replace:

    192.168.10.50 → your purifier IP

    mqtt-broker, mqttuser, mqttpass → your MQTT settings

    ha_net → your docker network

This loop:

    Polls purifier every 10 seconds

    Converts output to compact JSON

    Publishes to MQTT


## Home Assistant: MQTT sensors

If you use MQTT Discovery, HA will auto‑create entities.

If you prefer manual sensors:
```
sensor:
  - platform: mqtt
    name: "Philips PM2.5"
    state_topic: "philips/ac4220/state"
    value_template: "{{ value_json.pm25 }}"

  - platform: mqtt
    name: "Philips VOC"
    state_topic: "philips/ac4220/state"
    value_template: "{{ value_json.voc }}"

```
You can add fan control later using MQTT commands.