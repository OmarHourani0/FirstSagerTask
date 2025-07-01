import csv, json, random

def random_payload():
    return {
        "elevation": random.uniform(0, 10),
        "gear": random.choice([0, 1, 2, 3]),
        "height": random.uniform(0, 70),
        "height_limit": 70,
        "home_distance": random.random(),
        "horizontal_speed": random.uniform(0, 15),
        "is_near_area_limit": random.choice([0, 1]),
        "is_near_height_limit": random.choice([0, 1]),
        "latitude": 31.978 + random.uniform(-0.01, 0.01),
        "longitude": 35.831 + random.uniform(-0.01, 0.01),
        "rc_lost_action": random.choice([0, 1, 2]),
        "rid_state": random.choice([False, True]),
        "rth_altitude": 20 + random.uniform(-5, 5),
        "storage": {
            "total": random.uniform(0,60368000),  # exactly as your example
            "used": random.uniform(0,2000)        # exactly as your example
        },
        "total_flight_distance": random.uniform(0, 1000),
        "total_flight_sorties": random.randint(0, 20),
        "total_flight_time": random.uniform(0, 1000),
        "track_id": "",
        "vertical_speed": random.uniform(-5, 5),
        "wind_direction": random.randint(0, 359),
        "wind_speed": random.uniform(0, 20)
    }

with open("msgs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for i in range(1, 101):
        drone_id = f"drone{i:03d}"
        topic = f"thing/product/{drone_id}/osd"
        payload = json.dumps(random_payload())
        writer.writerow([topic, payload])

print("Wrote msgs.csv with 100 rows (storage fixed to your example).")
