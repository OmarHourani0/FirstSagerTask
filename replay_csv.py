import csv
import time
import paho.mqtt.client as mqtt

MQTT_BROKER_URL = "localhost"
MQTT_BROKER_PORT = 1883

client = mqtt.Client()
client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)

with open("msgs.csv", newline="") as f:
    reader = csv.reader(f)
    for topic, payload in reader:
        print(f"Publishing to {topic}")
        client.publish(topic, payload)
        time.sleep(0.1)  # slight delay to mimic real messages

print("Finished replaying msgs.csv.")
