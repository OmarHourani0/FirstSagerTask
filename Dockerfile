# Set the python version as a build-time argument
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    mosquitto \
    mosquitto-clients \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create the code directory
RUN mkdir -p /code
WORKDIR /code

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy the application source
COPY ./src /code

# Optional: collect static files (if needed)
RUN python manage.py collectstatic --no-input || true

# Copy entrypoint script
COPY ./boot/docker-run.sh /opt/docker-run.sh
RUN chmod +x /opt/docker-run.sh

CMD ["/opt/docker-run.sh"]
