#!/bin/bash

# Start Mosquitto broker in the background
mosquitto -c /etc/mosquitto/mosquitto.conf -d

# Activate virtual environment
source /opt/venv/bin/activate

# Change to code directory
cd /code

# Apply migrations
python manage.py migrate --no-input 

# Optional: Send dummy data (in background)
python send_fake_data.py &

# Set runtime variables
export RUNTIME_PORT=8000
export RUNTIME_HOST=0.0.0.0

# Start ASGI server with uvicorn (not gunicorn)
exec uvicorn task1.asgi:application --host $RUNTIME_HOST --port $RUNTIME_PORT
