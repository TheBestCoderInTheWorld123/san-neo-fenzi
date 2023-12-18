import paho.mqtt.client as mqtt
from  mqtt_preprocess import *
from mqtt_insert_pg import *
from model import *

# Broker details
broker_ip = "13.53.173.47"
port = 1883  # Default MQTT port, change if yours is different
topic = "devices/device_data"
username = "iot_dev"
password = "iot@developer"

# Callback when connected to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

# Callback when a message is received
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    msg_topic = msg.topic
    print(f"Topic: {msg_topic}\nMessage: {data}")
    records = preprocess(data=data)
    with session_scope() as session:
        insert_history_data(session, records)
    with session_scope() as session:
        insert_alert(session, records)


# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Assign the on_connect and on_message functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(broker_ip, port, 60)
# Loop forever, to continuously check for messages

client.loop_forever()