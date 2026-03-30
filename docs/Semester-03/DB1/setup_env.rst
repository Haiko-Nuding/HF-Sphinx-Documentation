Environment & SQL Basics
========================

This section covers the initial setup and the conceptual framework for working with relational databases.

Database Systems & Tools
------------------------
We use a Client-Server architecture:
* **Server:** MariaDB (Relational DBMS)
* **Client:** HeidiSQL or MySQL Workbench

SQL Sublanguages
----------------
* **DML (Data Manipulation Language):** Used for CRUD operations (Create, Read, Update, Delete).
* **DDL (Data Definition Language):** Used to define or modify the database structure (Tables, Schemas).
* **DCL (Data Control Language):** Used for rights management and security.

Practical Tasks
---------------
.. admonition:: Task 1: Environment Setup
   Verify your MariaDB connection and ensure the binary path is set:
   
   .. code-block:: bash

      mariadb --version

.. admonition:: Task 2: Data Import
   Create the databases ``F1DB`` and ``Uebungen`` and import the provided ``.sql`` dump files.