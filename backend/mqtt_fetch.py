import paho.mqtt.client as mqtt
from mqtt_preprocess import *
from mqtt_insert_pg import *
from model import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Broker details
broker_ip = "16.170.237.95"
port = 1883  # Default MQTT port, change if yours is different
topic = "devices/device_data"
username = "iot_dev"
password = "iot@developer"


# Callback when connected to the MQTT broker
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe(topic)


# Callback when a message is received
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode()
        msg_topic = msg.topic
        logging.info(f"Topic: {msg_topic}\nMessage: {data}")

        records = preprocess(data=data)

        with session_scope() as session:
            insert_history_data(session, records)

        with session_scope() as session:
            insert_alert(session, records)

    except Exception as e:
        logging.error(f"Error processing message: {e}")


# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Assign the on_connect and on_message functions
client.on_connect = on_connect
client.on_message = on_message


# Handle connection error
def on_connect_fail(client, userdata, flags, rc):
    logging.error(f"Failed to connect, return code {rc}")


client.on_connect_fail = on_connect_fail

# Connect to the broker
try:
    client.connect(broker_ip, port, 60)
except Exception as e:
    logging.error(f"Could not connect to MQTT broker: {e}")
    exit(1)  # Exit the script with an error code

# Start the loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    logging.info("MQTT client stopped manually")
except Exception as e:
    logging.error(f"MQTT client error: {e}")
