#!/bin/bash
set -e

echo "Starting Mosquitto..."
mosquitto -c /etc/mosquitto/mosquitto.conf -d

cd /code

echo "Applying Django migrations..."
python manage.py migrate --no-input

echo "Sending fake data..."
python send_fake_data.py &

echo "Starting ASGI server..."
exec uvicorn task1.asgi:application --host 0.0.0.0 --port 8000
