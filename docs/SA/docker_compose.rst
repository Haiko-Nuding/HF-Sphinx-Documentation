:hide-toc:

Docker Compose Amateur Guide
============================

Example 1: Basic Web Server
---------------------------

This is a straightforward Nginx setup, ideal for hosting static content. This setup uses the "default" network automatically created by Docker.

.. code-block:: yaml
   :caption: compose.yaml

   name: my-project-01

   services:
     web:
       image: nginx:latest
       ports:
         - "80:80"
       restart: always

How to Run It
^^^^^^^^^^^^^

1. Launch from the project directory:

   .. code-block:: bash

      docker-compose up -d

2. Open in your browser:

   .. code-block:: text

      http://localhost:80


Example 2: Network Isolation
----------------------------

This example uses a tiered setup defined in ``docker-compose.yaml``.

- The ``web`` service connects only to the ``frontend`` network.
- The ``api`` service connects to both ``frontend`` and ``backend`` networks.
- The ``db`` service connects only to the ``backend`` network.

This ensures the database is **isolated from the web tier**, while the API can access both networks.


.. code-block:: yaml
   :caption: compose.yaml

   name: network-test-project

   services:
     web:
       image: nginx:alpine
       ports:
         - "8080:80"
       networks:
         - frontend

     api:
       image: alpine
       command: /bin/sh -c "while true; do sleep 3600; done"
       networks:
         - frontend
         - backend

     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_PASSWORD: password123
       networks:
         - backend

   networks:
     frontend:
     backend:

Testing the Architecture
^^^^^^^^^^^^^^^^^^^^^^^^

After the containers are running:

.. code-block:: bash

   docker-compose up -d


**Test 1: Web → API (shared network)**
Services on the ``frontend`` network can resolve each other by name.

.. code-block:: bash

   docker-compose exec web ping -c 3 api

**Expected:** success


**Test 2: API → DB (dual-homed container)**
The API container is connected to both networks.

.. code-block:: bash

   docker-compose exec api ping -c 3 db

**Expected:** success


**Test 3: Web → DB (isolated)**
The web container must not reach the database.

.. code-block:: bash

   docker-compose exec web ping -c 3 db

**Expected:** failure

.. code-block:: text

   ping: bad address 'db'


Summary Table
^^^^^^^^^^^^^

+-----------------+--------------+--------------+-----------------------+
| Source          | Target       | Network      | Result                |
+=================+==============+==============+=======================+
| Web Container   | API          | frontend     | ✅ Allowed            |
+-----------------+--------------+--------------+-----------------------+
| API Container   | Database     | backend      | ✅ Allowed            |
+-----------------+--------------+--------------+-----------------------+
| Web Container   | Database     | N/A          | ❌ **Blocked**        |
+-----------------+--------------+--------------+-----------------------+


Example 3: Persistent Storage (Volumes & Bind Mounts)
-----------------------------------------------------

By default, data created inside a container is ephemeral. To save data permanently, we use **Volumes** and **Bind Mounts**.

- **Volumes:** Managed by Docker (best for Databases).
- **Bind Mounts:** Maps a local folder to the container (best for Source Code).



Project Structure
^^^^^^^^^^^^^^^^^

Ensure your project folder is organized like this before running the commands:

.. code-block:: text

   project03/
   ├── docker-compose.yaml
   └── html/
       └── index.html

Step 1: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     database:
       image: postgres:15-alpine
       environment:
         POSTGRES_PASSWORD: secretpassword
       volumes:
         # Named Volume: Data survives 'docker-compose down'
         - db_data:/var/lib/postgresql/data

     web-developer:
       image: nginx:alpine
       ports:
         - "8081:80"
       volumes:
         # Bind Mount: Maps your local "html" folder to Nginx
         # :ro means the container cannot modify your local files
         - ./html:/usr/share/nginx/html:ro

   volumes:
     db_data:

Step 2: The HTML File
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: html
   :caption: html/index.html

   <!DOCTYPE html>
   <html>
   <body>
       <h1>Docker Compose Success!</h1>
       <p>This file is served from a <strong>Bind Mount</strong>.</p>
   </body>
   </html>

Practical Exercise: "Hot Reloading"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open your terminal in the ``project03`` directory.

2. Run the stack:

   .. code-block:: bash

      docker-compose up -d

3. Visit your site in your browser:

   .. code-block:: text

      http://localhost:8081

4. **The Magic:** Open ``html/index.html`` in your code editor, change the text (e.g., change "Success" to "Updated!"), and save the file.

5. **Refresh your browser:** Notice that the changes appear instantly! This happens because the container is reading directly from your local folder.


Example 4: Environment Variables (.env)
---------------------------------------

Hardcoding passwords and configuration directly in your ``docker-compose.yaml`` is a security risk and makes the file hard to reuse. We use a **.env** file to store these variables separately.

- **Security:** Keep sensitive data out of your main logic.
- **Portability:** Change one file to update the entire stack's configuration.

Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   project04/
   ├── .env
   └── docker-compose.yaml

Step 1: The Environment File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a file named exactly ``.env``. Docker Compose automatically looks for this file.

.. code-block:: text
   :caption: .env

   # Database Settings
   DB_PASSWORD=super-secret-password
   DB_USER=admin_user

   # Versioning
   POSTGRES_TAG=15-alpine

Step 2: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

In this file, we use the ``${VARIABLE_NAME}`` syntax to pull values from the ``.env`` file.

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     db:
       # Using a variable for the image version tag
       image: postgres:${POSTGRES_TAG}
       environment:
         # Pulling credentials from the .env file
         POSTGRES_USER: ${DB_USER}
         POSTGRES_PASSWORD: ${DB_PASSWORD}
       volumes:
         - pgdata:/var/lib/postgresql/data

   volumes:
     pgdata:

Testing the Variables
^^^^^^^^^^^^^^^^^^^^^

After running the stack, you can verify that Docker correctly injected your "secret" variables.

1. Launch the service:

   .. code-block:: bash

      docker-compose up -d

2. Check the active environment variables inside the container:

   .. code-block:: bash

      docker-compose exec db env | grep POSTGRES

**Expected Output:**

.. code-block:: text

   POSTGRES_USER=admin_user
   POSTGRES_PASSWORD=super-secret-password

Summary of Benefits
^^^^^^^^^^^^^^^^^^^

+-----------------------+-------------------------------------------------------+
| Feature               | Why it matters                                        |
+=======================+=======================================================+
| **Security** | You can add ``.env`` to your .gitignore.                       |
+-----------------------+-------------------------------------------------------+
| **Flexibility** | Change ``POSTGRES_TAG`` to ``16-alpine`` in one place.      |
+-----------------------+-------------------------------------------------------+
| **Clarity** | Your YAML file stays clean and readable.                        |
+-----------------------+-------------------------------------------------------+

Example 5: Healthchecks & Startup Order
---------------------------------------

In a multi-container stack, some services must wait for others. For example, a Web App should not start until the Database is fully "Healthy," not just "Running."

- **Depends On:** Defines the order in which services start.
- **Healthcheck:** A command that runs inside the container to check if the service is actually working.



Project Structure
^^^^^^^^^^^^^^^^^

.. code-block:: text

   project05/
   └── docker-compose.yaml

Step 1: The Compose File
^^^^^^^^^^^^^^^^^^^^^^^^

This example shows a database providing a health status and a web service waiting for that status to be "healthy."

.. code-block:: yaml
   :caption: docker-compose.yaml

   services:
     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_PASSWORD: password123
       healthcheck:
         # This command checks if the database is accepting connections
         test: ["CMD-SHELL", "pg_isready -U postgres"]
         interval: 5s
         timeout: 5s
         retries: 5

     web:
       image: nginx:alpine
       depends_on:
         db:
           condition: service_healthy

Testing the Logic
^^^^^^^^^^^^^^^^^^^^^^^^

1. Run the stack:

   .. code-block:: bash

      docker-compose up -d

2. Watch the status updates in real-time:

   .. code-block:: bash

      docker-compose ps

**Observation:**
Initially, the ``web`` service will stay in a "created" or "starting" state. It will only transition to "running" once the ``db`` service status changes from ``(health: starting)`` to ``(healthy)``.

Summary of Settings
^^^^^^^^^^^^^^^^^^^

+-----------------+-----------------------------------------------------------+
| Key             | Description                                               |
+=================+===========================================================+
| ``test``        | The actual command used to verify the service is okay.    |
+-----------------+-----------------------------------------------------------+
| ``interval``    | How often to run the check (e.g., every 5 seconds).       |
+-----------------+-----------------------------------------------------------+
| ``retries``     | How many failures allowed before marking as "unhealthy".  |
+-----------------+-----------------------------------------------------------+
| ``condition``   | The requirement (e.g., wait for ``service_healthy``).     |
+-----------------+-----------------------------------------------------------+