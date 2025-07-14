import json
import time
import random
import paho.mqtt.publish as publish
import string

from droneData.classifiers import haversine

def fake_payload():
    length = 8
    track_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    lat = 31.9544 + random.uniform(-0.06, 0.06)
    lon = 35.9106 + random.uniform(-0.06, 0.06)
    height_limit = 500
    elevation = random.uniform(0, 550)
    if elevation > height_limit:
        near_height_limit = 1
    else:
        near_height_limit = 0
        
    return {
        "elevation": elevation,
        "gear": random.choice([0, 1, 2, 3]),
        "height": random.uniform(0, 10),
        "height_limit": height_limit,
        "home_distance": haversine(31.9544, 35.9106, lat, lon),
        "horizontal_speed": random.uniform(0, 15),
        "is_near_area_limit": random.choice([0, 1]),
        "is_near_height_limit": near_height_limit,
        "latitude": lat,
        "longitude": lon,
        "rc_lost_action": random.choice([0, 1, 2]),
        "rid_state": random.choice([False, True]),
        "rth_altitude": 20 + random.uniform(-5, 5),
        "storage": {
            "total": 60368000,
            "used": random.uniform(0, 2000)
        },
        "total_flight_distance": random.uniform(0, 1000),
        "total_flight_sorties": random.randint(0, 20),
        "total_flight_time": random.uniform(0, 1000),
        "track_id": track_id,
        "vertical_speed": random.uniform(0, 30),
        "wind_direction": random.randint(0, 359),
        "wind_speed": random.uniform(0, 20)
    }

drones = 100
DRONE_IDS = []

for i in range(1, drones + 1):
    drone_id = f"drone{i:03d}"
    DRONE_IDS.append(drone_id)
    topic = f"thing/product/{drone_id}/osd"
    payload = json.dumps(fake_payload())
    publish.single(topic, payload, hostname="localhost", port=1883)
    print(f"Sent to {topic}: {payload}")
    # print(f"Preparing to send data for {drone_id} ")
    time.sleep(0.05)  # Sleep to avoid overwhelming the MQTT broker