Docker Deployment
=================
This section provides instructions on how to deploy the project using Docker. To set up the Docker environment, follow these steps:

1. **Clone the Repository**:

   First, clone the repository to your local machine using Git:
   
.. code-block:: bash

    git clone https://github.com/OmarHourani0/FirstSagerTask.git
    cd FirstSagerTask

2. **Build the Docker Image**:

.. code-block:: bash

    docker-compose build

3. **Run the Docker Container**:

.. code-block:: bash

    docker-compose up -d

4. **Run Everything**:

.. code-block:: bash

    docker-compose exec web ./boot/docker-run.sh
    

4. **Access the Application**

   The app will be available at:

   http://localhost:8000