Setup Guide
===========

Here I will provide a brief guide on how to set up the Django project and make it run on your machine.

1. **Clone the Repository**:

   First, clone the repository to your local machine using Git:

.. code-block:: bash   

    git clone https://github.com/OmarHourani0/FirstSagerTask.git
    cd FirstSagerTask

2. **Install Dependencies**:

.. code-block:: bash

    python -m pip install --upgrade pip
    python -m venv django_venv
    source django_venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual environment activated and dependencies installed."

3. **Start Mosquitto broker in the background**:

.. code-block:: bash

    brew install mosquitto
    mosquitto -v &
    echo "Mosquitto broker started."

4. **Start Postgress DB Server**:

.. code-block:: bash

    brew install postgresql
    brew services start postgresql &
    echo "PostgreSQL server started."

5. **Start Redis DB Server**:

.. code-block:: bash

    brew install redis
    brew services start redis &
    echo "Redis server started."

6. **Apply DB Migrations**:

.. code-block:: bash

    python manage.py migrate
    echo "Database migrations applied."

7. **Create a Superuser**:

.. code-block:: bash

    python manage.py createsuperuser
    echo "Superuser created succesfully."

8. **Send Dummy Data**:

.. code-block:: bash

    python send_fake_data.py &
    echo "Dummy data sent to the database."

9. **Set runtime variables**:

.. code-block:: bash

    export RUNTIME_PORT=8000
    export RUNTIME_HOST=0.0.0.0


10. **Start ASGI server with uvicorn**:

.. code-block:: bash

    exec uvicorn task1.asgi:application --host $RUNTIME_HOST --port $RUNTIME_PORT