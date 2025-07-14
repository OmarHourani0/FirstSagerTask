Configuration
=============

The configuration when it comes to the running ports and everything of this Django project is as follows:

**Services and Ports**:

- **Django Application**: Runs on port `8000`
- **Redis**: Runs on port `6379`
- **PostgreSQL**: Runs on port `5432`
- **Mosquitto MQTT Broker**: Runs on port `1883`

+----------------+--------+------------------------------------------+
| Service        | Port   | Description                              |
+================+========+==========================================+
| Django App     | 8000   | Web application and API interface        |
+----------------+--------+------------------------------------------+
| Redis          | 6379   | Django Channels backend                  |
+----------------+--------+------------------------------------------+
| PostgreSQL     | 5432   | Database service                         |
+----------------+--------+------------------------------------------+
| Mosquitto      | 1883   | MQTT broker for drone telemetry          |
+----------------+--------+------------------------------------------+
