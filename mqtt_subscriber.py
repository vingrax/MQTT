import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import redis

# Redis Connection
redis_host = "redis"
redis_port = 6379
redis_db = 0

redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

def store_latest_reading(sensor_id, reading):
    # Add the new reading to the list
    redis_client.lpush(sensor_id, reading)
    # Trim the list to keep only the latest ten readings
    redis_client.ltrim(sensor_id, 0, 9)

# MQTT Broker Information
broker_address = "mqtt5"
broker_port = 1883

# MongoDB Connection
mongodb_uri = "mongodb://mqtt:mqttpass@mongodb:27017/"
db_name = "mqtt_data"
collection_name = "sensor_readings"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("sensors/#")  # Subscribe to all sensor topics

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    try:
        sensor_data = json.loads(payload)
        store_in_mongodb(sensor_data)
        print(f"Received: {sensor_data}")
    except json.JSONDecodeError:
        print("Invalid JSON payload")

def store_in_mongodb(sensor_data):
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(sensor_data)
    client.close()
    store_latest_reading(sensor_data["sensor_id"], sensor_data['value'])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port)

client.loop_forever()
