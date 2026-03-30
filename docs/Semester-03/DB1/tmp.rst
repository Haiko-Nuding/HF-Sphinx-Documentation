
Arbeitsblatt 01
===============

DB über CLI erstellen:
----------------------
# cli auf utf-8 stellen
chcp 65001


# Login
mariadb -u root -p

# create DB inside MariaDB
CREATE DATABASE uebungen2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;


# import sql file:
mariadb -u root -p [DB-Name] < "C:\Pfad\zu\deiner\datei.sql"


CLI - Maria DB Verbinden
------------------------

# Login - Connect - Show databases - USE DB

SHOW DATABASES;
USE [DB-NAME]


Navigate trhough a new DB in MariaDB
------------------------------------

# you need to be in MariaDB and select a DB

SHOW TABLES;

DESCRIBE [TABLE-NAME]

HELP-FUL Selects
----------------

# Select all circuits that have no previous names (NULL values)
SELECT * FROM circuit WHERE previous_names IS NULL;  

# Count the number of circuits that have no previous names
SELECT COUNT(*) FROM circuit WHERE previous_names IS NULL;
