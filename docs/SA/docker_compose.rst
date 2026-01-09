:hide-toc:

Docker Compose Project Guide
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
-------------

1. **Launch**: Open PowerShell in the project directory and run:

   .. code-block:: bash

      docker-compose up -d

2. **Verify**: Open your browser to ``http://localhost``. If Port 80 is blocked by another Windows service, change the ports line to ``"8080:80"`` and visit ``http://localhost:8080``.


Example 2: Network Isolation
----------------------------

This example demonstrates a "tiered" architecture. We use custom networks to ensure the Database is unreachable from the web-tier, providing a layer of security.



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
------------------------

Once the containers are running with ``docker-compose up -d``, perform these tests to verify network logic.

**Test 1: Web to API (Shared Network)**
Since both share the ``frontend`` network, they can communicate via service name.

* **Command**: ``docker compose exec web ping -c 3 api``
* **Expected Result**: **Success**.

**Test 2: API to DB (Shared Network)**
The API container sits on both networks, allowing it to "see" the database.

* **Command**: ``docker compose exec api ping -c 3 db``
* **Expected Result**: **Success**.

**Test 3: Web to DB (Isolated)**
This is the security test. The web container has no path to the database.

* **Command**: ``docker compose exec web ping -c 3 db``
* **Expected Result**: **Failure**. You should see ``ping: bad address 'db'``.

Summary Table
-------------

+-----------------+--------------+--------------+-----------------------+
| Source          | Target       | Network      | Result                |
+=================+==============+==============+=======================+
| Web Container   | API          | frontend     | ✅ Allowed            |
+-----------------+--------------+--------------+-----------------------+
| API Container   | Database     | backend      | ✅ Allowed            |
+-----------------+--------------+--------------+-----------------------+
| Web Container   | Database     | N/A          | ❌ **Blocked**        |
+-----------------+--------------+--------------+-----------------------+