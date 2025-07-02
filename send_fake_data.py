import json
import time
import random
import paho.mqtt.publish as publish
import string

from droneData.classifiers import haversine


def fake_payload():
    length = 8
    track_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    lat = 31.000 + random.uniform(-0.06, 0.06)
    lon = 37.000 + random.uniform(-0.06, 0.06)
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
        "home_distance": haversine(31.000, 39.000, lat, lon),
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

DRONE_IDS = [
    "drone001", "drone002", "drone003", "drone004", "drone005", "drone006", "drone007", "drone008", "drone009", "drone010",
    "drone011", "drone012", "drone013", "drone014", "drone015", "drone016", "drone017", "drone018", "drone019", "drone020",
    "drone021", "drone022", "drone023", "drone024", "drone025", "drone026", "drone027", "drone028", "drone029", "drone030",
    "drone031", "drone032", "drone033", "drone034", "drone035", "drone036", "drone037", "drone038", "drone039", "drone040",
    "drone041", "drone042", "drone043", "drone044", "drone045", "drone046", "drone047", "drone048", "drone049", "drone050",
    "drone051", "drone052", "drone053", "drone054", "drone055", "drone056", "drone057", "drone058", "drone059", "drone060",
    "drone061", "drone062", "drone063", "drone064", "drone065", "drone066", "drone067", "drone068", "drone069", "drone070",
    "drone071", "drone072", "drone073", "drone074", "drone075", "drone076", "drone077", "drone078", "drone079", "drone080",
    "drone081", "drone082", "drone083", "drone084", "drone085", "drone086", "drone087", "drone088", "drone089", "drone090",
    "drone091", "drone092", "drone093", "drone094", "drone095", "drone096", "drone097", "drone098", "drone099", "drone100"
]

for id in DRONE_IDS:
    topic = f"thing/product/{id}/osd"
    payload = json.dumps(fake_payload())
    publish.single(topic, payload, hostname="localhost", port=1883)
    print(f"Sent to {topic}: {payload}")
    time.sleep(0.05)
