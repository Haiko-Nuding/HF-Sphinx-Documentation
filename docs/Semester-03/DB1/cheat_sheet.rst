==========================================================
MariaDB CLI Cheat Sheet - Modul DB I (gibb HF I & T)
==========================================================

----------------------------------------------------------
1. AB1: Umgebung & Vorbereitung (DDL & System)
----------------------------------------------------------

Datenbanken verwalten:
----------------------
CREATE DATABASE f1db;                   -- Neue DB erstellen
SHOW DATABASES;                         -- Alle DBs auflisten
USE f1db;                               -- In eine DB wechseln
SHOW TABLES;                            -- Alle Tabellen der aktuellen DB anzeigen
DESCRIBE circuits;                      -- Struktur einer Tabelle anzeigen (Spalten, Typen)

SQL-Skript (Dump) importieren (aus der Windows CMD):
----------------------------------------------------
mariadb -u root -p f1db < C:\Pfad\zu\f1db.sql

----------------------------------------------------------
2. AB2: Lesen und Auswerten (DML - SELECT)
----------------------------------------------------------

Grundlegende Abfragen (Aufgaben 1-3):
-------------------------------------
SELECT name FROM circuits;                          -- Einzelne Spalte
SELECT name, location FROM circuits;                -- Mehrere Spalten
SELECT name AS "Strecke", location AS "Ort" FROM circuits; -- Umbenennen (Alias)

Filtern und Sortieren (Aufgaben 4-10):
--------------------------------------
SELECT * FROM circuits WHERE lat < 0;               -- Filtern (Südhalbkugel)
SELECT * FROM circuits WHERE name LIKE 'A%';        -- Wildcards (Beginnt mit A)
SELECT * FROM circuits WHERE alt_name IS NULL;      -- Auf NULL prüfen
SELECT DISTINCT country_id FROM circuits;           -- Duplikate eliminieren
SELECT * FROM circuits ORDER BY name DESC;          -- Sortieren (Absteigend)

Aggregation & Gruppierung (Aufgaben 9-10):
------------------------------------------
SELECT country_id, COUNT(*) FROM circuits GROUP BY country_id; -- Zählen pro Land
SELECT country_id, COUNT(*) AS anzahl FROM circuits 
GROUP BY country_id ORDER BY anzahl DESC;           -- Kombiniert mit Sortierung

----------------------------------------------------------
3. AB3: Joins, Datenänderung & Transaktionen
----------------------------------------------------------

Mehrtabellenabfragen (JOINs):
-----------------------------
-- Aufgabe 2: Rennen mit Streckennamen verknüpfen
SELECT r.year, r.name, c.name 
FROM race r 
INNER JOIN circuits c ON r.circuit_id = c.id;

-- LEFT JOIN (Falls auch Daten ohne Treffer erscheinen sollen)
SELECT r.name, r.year 
FROM race r 
LEFT JOIN race_data rd ON r.id = rd.race_id;

Daten verändern (DML - INSERT, UPDATE, DELETE):
-----------------------------------------------
INSERT INTO race (id, year, name) VALUES (2000, 2026, 'Test GP'); -- Einfügen
UPDATE teams SET name = 'Last' WHERE name = 'First';              -- Ändern
DELETE FROM race_data WHERE race_id < 500;                        -- Löschen

Strings verketten & Casten (Aufgabe 10):
----------------------------------------
SELECT CONCAT(name, ' (', CAST(turns AS CHAR), ')') FROM circuits;

Transaktionen (Aufgaben 13-15):
-------------------------------
SET AUTOCOMMIT = 0;                     -- Autocommit für Transaktions-Session aus
START TRANSACTION;                      -- Transaktion beginnen

-- Deine Änderungen hier (z.B. DELETE oder INSERT)

SELECT * FROM race WHERE id = 2000;     -- Kontrolle (sieht nur deine Session)

COMMIT;                                 -- Dauerhaft speichern
-- ODER --
ROLLBACK;                               -- Alles rückgängig machen

----------------------------------------------------------
4. Nützliche CLI-Helfer
----------------------------------------------------------
system cls                              -- Screen löschen (Windows)
\c                                      -- Aktuellen (falschen) Befehl abbrechen
exit                                    -- MariaDB verlassen
\! help                                 -- Hilfe zu Systembefehlen