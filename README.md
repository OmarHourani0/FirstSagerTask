# First Sager Task: Real-Time Drone Telemetry System

This project implements a Django-based system for receiving, processing, and visualizing real-time drone telemetry data using MQTT and WebSockets.

The system supports multiple drones publishing telemetry data. The backend stores the data in a PostgreSQL database, processes it via MQTT, and serves it to users through dynamic dashboards, REST-like API endpoints, and WebSocket connections.

---

## Features

- Real-time telemetry updates via Django Channels and WebSockets
- MQTT integration for high-throughput telemetry ingestion
- PostgreSQL-backed data persistence
- Redis-backed channel layer for scalable asynchronous communication
- Interactive drone tracking map and telemetry dashboards
- Custom query interface for advanced telemetry inspection
- Modular and dockerized deployment workflow

---

## Services and Ports

| Service       | Port  | Description                         |
|---------------|-------|-------------------------------------|
| Django App    | 8000  | Web application and API interface   |
| Redis         | 6379  | Django Channels backend             |
| PostgreSQL    | 5432  | Database service                    |
| Mosquitto     | 1883  | MQTT broker for drone telemetry     |

---

## Web Interface Endpoints

All endpoints are available at `http://localhost:8000/`

### Authentication and Dashboards

- `/`  
  Login page

- `/data/`  
  Dashboard displaying real-time data for all drones (login required)

### Visualization and Query Tools

- `/drone-map/`  
  Interactive map showing real-time drone positions

- `/drone-query/`  
  Custom telemetry data queries per drone

### Filtered Data Views

- `/drone-list/`  
  List of all drone IDs with coordinates

- `/nearby-drones/`  
  Drones located within 5 km of the reference point (31.000, 39.000)

- `/danger-list/`  
  List of drones marked with a danger classification and explanation

---

## API Endpoints

- `/api/flight-path/<drone_id>/`  
  Returns the full flight path and current position of the specified drone

- `/api/all-flight-paths/`  
  Returns flight paths and positions of all drones

---

## Custom Query Format

To extract specific fields from a drone, navigate to `/drone-query/` and enter a string in the following format:
    
    'drone009-GEAR-HEIGHT-VERTICAL_SPEED-HEIGHT-ELEVATION-CLASSIFICATION'
- The first token is the `drone_id` (required)
- All other tokens correspond to telemetry fields you wish to retrieve (dash `-` separated)

---

## Available Data Fields

### Position and Motion

- `latitude`
- `longitude`
- `elevation`
- `height`
- `height_limit`
- `home_distance`
- `horizontal_speed`
- `vertical_speed`
- `wind_speed`
- `wind_direction`

### Status Flags and Modes

- `gear`
- `is_near_area_limit`
- `is_near_height_limit`
- `rc_lost_action`
- `rid_state`
- `rth_altitude`

### Storage

- `storage_total`
- `storage_used`

### Flight Summary

- `total_flight_distance`
- `total_flight_sorties`
- `total_flight_time`

### Miscellaneous

- `track_id`
- `classification`
- `timestamp`

---

## Local Development Setup

To run the system locally, ensure the following dependencies are installed and running:

### Step-by-Step Commands


### Start MQTT broker
```
mosquitto -v
```
### Start Redis
```
brew services start redis
```

### Start PostgreSQL
```
brew services start postgresql
```

### Apply Django migrations
```
python manage.py migrate
```

### Run the development ASGI server
```
uvicorn task1.asgi:application --host 127.0.0.1 --port 8000
```

## Docker Depoloyment Setup
### Build Container
```
docker build -t sager-task-1 .
```

### Run Container
```
docker run -p 8000:8000 sager-task-1
```
