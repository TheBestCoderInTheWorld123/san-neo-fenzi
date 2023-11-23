import re
import json
import paho.mqtt.client as mqtt
import psycopg2
from urllib.parse import quote_plus
import sys
from datetime import datetime
# data = """IMEI:"862174069140333",AQ:">10.0",HUM:"51",TMP:"32",TIM:"2023/11/21,13:02"
# IMEI:"862174069140333",AQ:">10.0",HUM:"51",TMP:"32",TIM:"2023/11/21,13:02"
# IMEI:"862174069140333",AQ:">10.0",HUM:"51",TMP:"32",TIM:"2023/11/21,13:02"
# IMEI:"862174069140333",AQ:">10.0",HUM:"51",TMP:"32",TIM:"2023/11/21,13:03"
# --"""
# data = "IMEI:'862174069140333',AQ:'>10.0',HUM:'51',TMP:'32',TIM:'2023/11/21,13:02'"
def preprocess(data):
    data_split = data.split(',')
    print(data_split)
    record =[]
    imei = ''
    j = 0 
    record_dict = {}
    for i in range(len(data_split)):
        status =''
        
        data_split_split=data_split[i].split(':')
        print(data_split_split)
        if i == 0 :
            imei = data_split_split[1].replace("'",'')
            print(imei)
        if i >0 and i < len(data_split)-2:
            record_value = ''
            print(data_split_split[1])
            for  character_in_data in data_split_split[1]:
                if character_in_data not in '.0123456789':
                    status += character_in_data
                else:
                    record_value += character_in_data
            # record.append(data_split[0].split(':')[1], )
            status = status.replace("'","")
            # print(record_value)
            date_str = (data_split[len(data_split)-2].split(':')[1] +" "+ data_split[len(data_split)-1]).strip("'")
            date_time  = datetime.strptime(date_str,'%Y/%m/%d %H:%M')
            record.append([{'IMEI': imei}, {data_split[i].split(':')[0]: record_value}, {'status': status}, {'date_time': date_time}])
            record_dict[j]=record[-1]
            j+=1
    return record_dict
    # if i == len(data_split)-1:
    #     date_str = (data_split[len(data_split)-2].split(':')[1] +" "+ data_split[len(data_split)-1]).strip("'")
    #     date_time  = datetime.strptime(date_str,'%Y/%m/%d %H:%M')
    #     # print(date_time)
# print(record)

# print(record_dict)
# print(record_dict[0][1]('AQ'))
# sys.exit()
# pattern = r"IMEI:\"(.*?)\",AQ:\"(.*?)\",HUM:\"(.*?)\",TMP:\"(.*?)\",TIM:\"(.*?)\""
# matches = re.findall(pattern, data)

# for match in matches:
#     imei, aq, hum, tmp, tim = match
#     print(f"IMEI: {imei}, AQ: {aq}, HUM: {hum}, TMP: {tmp}, TIM: {tim}")

# json_data = []
# for match in matches:
#     imei, aq, hum, tmp, tim = match

#     json_data.append({
#         "imei": imei,
#         "aq": aq,
#         "hum": hum,
#         "tmp": tmp,
#         "tim": tim
#     })

# print(json.dumps(json_data))

# # MQTT Broker details
# mqtt_broker = "13.53.173.47"
# mqtt_port = 1883
# mqtt_topic = "devices/device_data"
# mqtt_username = "iot_dev"
# mqtt_password = "iot@developer"

# PostgreSQL database details
# db_host = '51.20.144.184'
# db_username = 'iot_dev'
# db_password = 'iod@developer'
# db_name = 'iot_penguin'
# encoded_password = quote_plus(db_password)
# db_url = f'postgresql://{db_username}:{encoded_password}@{db_host}/{db_name}'

# Function to insert data into PostgreSQL
# def insert_into_db(data):
#     try:
#         conn = psycopg2.connect(db_url)
#         cursor = conn.cursor()
#         # Assuming your data is a simple key-value pair, adjust the query as per your data structure
#         query = "INSERT INTO your_table_name (column1, column2) VALUES (%s, %s)"
#         cursor.execute(query, (data['key1'], data['key2']))
#         conn.commit()
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         print("Database error:", e)

# # MQTT callback functions
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))
#     client.subscribe(mqtt_topic)

# def on_message(client, userdata, msg):
#     print(f"Message received on topic {msg.topic}: {msg.payload}")
#     # Convert payload to Python dictionary
#     data = json.loads(msg.payload)
#     print(data)
#     # insert_into_db(data)

# # Setup MQTT client
# client = mqtt.Client()
# client.username_pw_set(mqtt_username,mqtt_password)
# client.username_pw_set(mqtt_username, mqtt_password)
# client.on_message = on_message(client)

# # Connect to MQTT broker and subscribe to the specified topic
# client.connect(mqtt_broker)
# client.subscribe(mqtt_topic)
# client.loop_start()

