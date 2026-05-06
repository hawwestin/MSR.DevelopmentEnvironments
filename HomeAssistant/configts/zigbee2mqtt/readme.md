References

- [Instuction about configuration content](https://www.zigbee2mqtt.io/guide/configuration/)
- [Configuration of your adapter](https://www.zigbee2mqtt.io/guide/adapters/)

Check currently supported firmware versions. You may need to update firmware on your antena / adapter / dongle. 

Each section of configuration.yaml have dedicated page that expand in more advanced options
- Section [MQTT](https://www.zigbee2mqtt.io/guide/configuration/mqtt.html)
- Section [Serial](https://www.zigbee2mqtt.io/guide/configuration/adapter-settings.html)
- Advanced is placed in many sections as part of documentation [advanced](https://www.zigbee2mqtt.io/guide/configuration/zigbee-network.html)
- more options for [Frontend](https://www.zigbee2mqtt.io/guide/configuration/frontend.html)
- not default section [Devices](https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html)
- Over the air firmware upgrades [OTA](https://www.zigbee2mqtt.io/guide/configuration/ota-device-updates.html)
- Device [availability](https://www.zigbee2mqtt.io/guide/configuration/device-availability.html)
- Integration with [homeassistant](https://www.zigbee2mqtt.io/guide/configuration/homeassistant.html) 
 
All Settings are documented in a big list of Yaml syntax https://www.zigbee2mqtt.io/guide/configuration/all-settings.html#advanced 

## Configuration Update
References
- Official docs https://www.zigbee2mqtt.io/guide/configuration/configuration-update.html

**Caution !**\
Do not edit the version setting manually. If you do, you run the risk of corrupting your configuration.yaml, the migration system may no longer work properly.