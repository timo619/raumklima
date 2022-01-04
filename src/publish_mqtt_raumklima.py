#!/usr/bin/python3
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from rs500reader.reader import Rs500Reader
import json

if len(sys.argv) - 1 == 1:
    arg = sys.argv[1]
else:
    arg = ""

if arg == "-discover":
    #Wenn True erstellt/updated oder löscht Sensoren
    CONFIG = True
    #Wenn False löscht Sensoren
    CREATE_SENSOR = True
elif arg == "-delete":
    CONFIG = True
    CREATE_SENSOR = False
else:
    CONFIG = False
    CREATE_SENSOR = True

broker = 'localhost'
topic_base = 'homeassistant/sensor/raumklima/'


#Namen der Räume
room = {
    1: "Balkon",
    2: "Flur",
    3: "Badezimmer",
    4: "Büro",
    5: "Küche",
    6: "Abstellkammer",
    7: "Wohnzimmer",
    8: "Schlafzimmer"
    }


def send_mqtt(topic, payload):
    try:
        payload = json.dumps(payload)
        publish.single(topic, payload=payload, qos=0, retain=False, hostname=broker,
        port=1883, client_id="", keepalive=60, will=None, 
        tls=None,
        protocol=mqtt.MQTTv311, transport="tcp")
    except Exception as e:
        print("Error", e)


if CONFIG == False:
    reader = Rs500Reader()
    data = reader.get_data()

for i in range(1, 9, 1):

    if CONFIG == True:
        topic_temp = topic_base + "ch{}_temp/config".format(i)
        topic_hum = topic_base + "ch{}_hum/config".format(i)
        if CREATE_SENSOR == True:
            config_payload_temperature = {"device_class": "temperature", 
                "name": "{}_Ch{}_temp".format(room[i], i), 
                "state_topic": "homeassistant/sensor/raumklima/"+"ch{}/state".format(i), 
                "unit_of_measurement": "°C", 
                "value_template": "{{ value_json.temperature}}" }
            config_payload_humidity = {"device_class": "humidity", 
                "name": "{}_Ch{}_hum".format(room[i], i), 
                "state_topic": "homeassistant/sensor/raumklima/"+"ch{}/state".format(i), 
                "unit_of_measurement": "%", 
                "value_template": "{{ value_json.humidity}}" }
            print("Sensor created:", topic_temp)
            print("Sensor created:", topic_hum)
        else:
            config_payload_temperature = ""
            config_payload_humidity = ""
            print("Sensor deleted:", topic_temp)
            print("Sensor deleted:", topic_hum)

        send_mqtt(topic_temp, payload = config_payload_temperature)
        send_mqtt(topic_hum, payload = config_payload_humidity)


    else:
        topic_ch = topic_base + "ch{}/state".format(i)
        chan_data = data.get_channel_data(i)
        data_dict = {"temperature":chan_data.temperature, "humidity": chan_data.humidity}
        send_mqtt(topic_ch, payload = data_dict)

        print(topic_base+"ch{}/temperature: {} °C".format(i, chan_data.temperature))
        print(topic_base+"ch{}/humidity: {} %".format(i, chan_data.humidity))




