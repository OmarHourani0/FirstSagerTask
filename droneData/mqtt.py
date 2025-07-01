import json
import threading
import paho.mqtt.client as mqtt
from .models import DroneData
from .classifiers import classify
from django.utils import timezone
from django.conf import settings

DRONE_IDS = getattr(settings, 'DRONE_IDS', [])
MQTT_BROKER_URL = getattr(settings, 'MQTT_BROKER_URL', 'localhost')
MQTT_BROKER_PORT = getattr(settings, 'MQTT_BROKER_PORT', 1883)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code:", rc)
    for drone_id in DRONE_IDS:
        topic = f"thing/product/{drone_id}/osd"
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        drone_id = msg.topic.split("/")[2]
        label = classify(data)

        DroneData.objects.create(
            drone_id=drone_id,

            # Position & motion
            latitude=data['latitude'],
            longitude=data['longitude'],
            elevation=data['elevation'],
            height=data['height'],
            height_limit=data['height_limit'],
            home_distance=data['home_distance'],
            horizontal_speed=data['horizontal_speed'],
            vertical_speed=data['vertical_speed'],
            wind_speed=data['wind_speed'],
            wind_direction=data['wind_direction'],

            # Status flags & modes
            gear=data['gear'],
            is_near_area_limit=bool(data['is_near_area_limit']),
            is_near_height_limit=bool(data['is_near_height_limit']),
            rc_lost_action=data['rc_lost_action'],
            rid_state=bool(data['rid_state']),
            rth_altitude=data['rth_altitude'],

            # Storage
            storage_total=data['storage']['total'],
            storage_used=data['storage']['used'],

            # Flight summary
            total_flight_distance=data['total_flight_distance'],
            total_flight_sorties=data['total_flight_sorties'],
            total_flight_time=data['total_flight_time'],

            # Misc
            track_id=data.get('track_id', ''),

            # Classification
            classification=label
        )

    except Exception as e:
        print(f"Error processing MQTT message on {msg.topic}: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT)  # change to your broker IP/port

    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True
    thread.start()