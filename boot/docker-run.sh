#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Change to code directory
cd /code

# Apply migrations
python manage.py migrate --no-input 

# Create admin user if script exists
python manage.py auto_admin

# Set runtime variables
export RUNTIME_PORT=8000
export RUNTIME_HOST=0.0.0.0

# Collect static files
python manage.py collectstatic --no-input 

# Run development server (corrected)
python manage.py runserver $RUNTIME_HOST:$RUNTIME_PORT
