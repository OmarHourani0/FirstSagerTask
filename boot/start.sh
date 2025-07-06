#!/bin/bash

python -m pip install --upgrade pip
python -m venv django_venv
source django_venv/bin/activate
pip install -r requirements.txt
echo "Virtual environment activated and dependencies installed."



# Start Mosquitto broker in the background
brew install mosquitto
mosquitto -v &
echo "Mosquitto broker started."


brew install redis            
brew services start redis &
echo "Redis server started."

brew install postgresql
brew services start postgresql &
echo "PostgreSQL server started."

# Apply migrations
python manage.py migrate --no-input 

# Optional: Send dummy data (in background)
python send_fake_data.py &
echo "Django migrations applied and data sent."

# Set runtime variables
export RUNTIME_PORT=8000
export RUNTIME_HOST=0.0.0.0

# Start ASGI server with uvicorn (not gunicorn)
exec uvicorn task1.asgi:application --host $RUNTIME_HOST --port $RUNTIME_PORT
