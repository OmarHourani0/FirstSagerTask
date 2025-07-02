#!/bin/bash

# Start Mosquitto broker in the background
mosquitto -c /etc/mosquitto/mosquitto.conf -d

# Activate virtual environment
source /opt/venv/bin/activate

# Change to code directory
cd /code

# Apply migrations
python manage.py migrate --no-input 

# Set runtime variables
export RUNTIME_PORT=8000
export RUNTIME_HOST=0.0.0.0

python send_fake_data.py

# Run development server
gunicorn task1.wsgi:application --bind $RUNTIME_HOST:$RUNTIME_PORT
