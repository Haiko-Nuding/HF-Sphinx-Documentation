Docker
======

Introduction
------------
Docker is a platform that allows you to package applications and their dependencies into lightweight, portable containers. Containers isolate applications from the host system, ensuring consistent behavior across environments.

.. admonition:: Key Concepts

   **Containers:** Running instances of applications, isolated but sharing the host OS kernel.

   **Images:** Read-only templates used to create containers. Images can include application code, libraries, and system tools.

   **Volumes:** Persistent storage for containers. Volumes allow data to survive container restarts or deletion.

   **Networks:** Define how containers communicate with each other or the outside world.



Why Use Docker
~~~~~~~~~~~~~~

**Consistency:** Applications run the same way everywhere.

**Isolation:** Multiple applications can run on the same host without conflicts.

**Portability:** Containers can be deployed on any system with Docker.

**Efficiency:** Lightweight compared to virtual machines.




Docker Basics
-------------
Minimal examples to illustrate key concepts:

Run a container:

.. code-block:: bash

   docker run hello-world

List running containers:

.. code-block:: bash

   docker ps

Build an image from a Dockerfile:

.. code-block:: bash

   docker build -t myapp:latest .

Attach a volume to preserve data:

.. code-block:: bash

   docker run -v mydata:/data ubuntu

Inspect a running container:

.. code-block:: bash

   docker inspect <container_id>