import paho.mqtt.client as mqtt
import random
import json
import time
client = mqtt.Client("sensor_publisher")
broker_address = "mqtt5"  # Replace with your broker's IP or hostname
port = 1883  # Default MQTT port
client.connect(broker_address, port)
def generate_sensor_data(sensor_id):
    data = {
        "sensor_id": sensor_id,
        "value": str(random.uniform(0, 100)),  # Replace with your logic to generate sensor values
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S')
    }
    return json.dumps(data)

while True:
    temperature_data = generate_sensor_data("temperature_sensor")
    humidity_data = generate_sensor_data("humidity_sensor")

    client.publish("sensors/temperature", temperature_data)
    client.publish("sensors/humidity", humidity_data)

    time.sleep(10)  # Publish every 10 seconds

