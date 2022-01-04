
# Access room climate station dnt RoomLogg Pro in linux (Raspberry Pi)

The climate station is also distributed as Raumklimastation RS500 from ELV or HP3000 from Ambient Weather, Manufacturer in China: Fine Offset
The software was written by (https://github.com/juergen-rocks/raumklima/issues/40).

![Picture of climate station](https://github.com/timo619/raumklima/master/doc/img/climate-station.jpg)

## More information in german:

Etwas ausführlicher als hier und mit mehr Hintergrundinformationen wird die Verwendung der RS 500 mit einem Raspberry Pi hier beschrieben:

- [juergen.rocks: ELV Raumklimastation RS 500 mit Raspberry Pi unter Linux auslesen](https://juergen.rocks/art/elv-raumklimastation-rs500-raspberry-pi-linux.html "juergen.rocks: ELV Raumklimastation RS 500 mit Raspberry Pi unter Linux auslesen")
- [juergen.rocks: ELV Raumklimastation RS 500 mit Icinga 2 auswerten und überwachen](https://juergen.rocks/art/elv-raumklimastation-rs500-icinga2.html "juergen.rocks: ELV Raumklimastation RS 500 mit Icinga 2 auswerten und überwachen")


## Motivation

Fully stand-alone climate (temperature + humidity) station with a main display a displays on all remote sensors, which can be accessed via USB. The values can be distributed via MQTT to a homeassistant instance. 

```
                                            +-----------------> MQTT to HomeAssistant (publish_mqtt_raumklima.py)
                                            |
  +-----------------+               +--------------+
  | Climate station | <--- USB ---> | Raspberry Pi | ---------> Web-interface via HomeAssistant (not in this repository)
  +-----------------+               +--------------+


```


## Reverse Engineering

See https://github.com/juergen-rocks/raumklima


## What works?

Temperature and humidity for all 8 channels can be read via USB.


## Whats not working?

- only one climate station
- configuration can not be changed


## How it fits together?

### Raspberry Pi with climate station

Install:

- Raspbian Stretch
- make
- gcc
- python3
- python3-dev
- python3-virtualenv
- libusb-1.0-0-dev
- libudev-dev

virtualenv::

- `pip install -r requirements-rs500reader.txt`

------
Add:
`nano /etc/udev/rules.d/50-hid.rules`

```
[Content]
SUBSYSTEM=="usb", ATTR{idVendor}=="0483", ATTR{idProduct}=="5750", MODE="0666"
```

restart udev --> 
`sudo udevadm trigger`
------
Add to crontab-file (via crontab -e):
```
@reboot python raumklima/src/publish_mqtt_raumklima.py -discover> /dev/null 2>&1;
* *  *   *   *     python raumklima/src/publish_mqtt_raumklima.py > /dev/null 2>&1;
0,30 *  *   *   *     python raumklima/src/publish_mqtt_raumklima.py -discover> /dev/null 2>&1;
```
-------
Install Docker:
`sudo apt-get install docker.io docker-compose`
-------
Install Home Assistant:
`sudo docker run -d   --name homeassistant   --privileged   --restart=unless-stopped   -e TZ=Europe/Berlin   -v /home/pi/homeassistant:/config   --network=host   ghcr.io/home-assistant/home-assistant:stable`
-------
Install Telegraf-InfluxDB-Grafana alltogether:
`git clone https://github.com/alekece/tig-stack`
`cd tig-stack`
`sudo docker-compose up -d`
-------
Create influxDB Database with the name homeassistant
`sudo docker exec -it influxdb /bin/bash`
`influx`
`CREATE DATABASE homeassistant`




