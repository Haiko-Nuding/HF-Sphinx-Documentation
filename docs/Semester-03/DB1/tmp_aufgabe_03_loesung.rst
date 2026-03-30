==========================================================
Modul DB I - AB3: Mehrtabellenabfragen & Datenveränderung
==========================================================

:Thema: Joins, DML (Insert, Update, Delete) und Transaktionen
:Datenbank: f1db (MariaDB)
:Format: Lösungen für SQL-Aufgaben

Aufgaben zu JOIN
================

Aufgabe 1 - Datenmodell
-----------------------
*Aufgabe: Zeichnen Sie eine Übersicht der Datenbank «f1db», auf welcher man sieht, wie die Tabellen zusammenhängen (Fokus auf race und race_data).*



.. code-block:: sql

   # Logische Verknüpfungen (ER-Modell):
   # race (circuit_id)          -> circuit (id)
   # race (grand_prix_id)       -> grand_prix (id)
   # race_data (race_id)        -> race (id)
   # race_data (driver_id)      -> driver (id)
   # race_data (constructor_id) -> constructor (id)

Aufgabe 2 - Joins
-----------------
*Aufgabe: Geben Sie alle Jahreszahlen, Namen aller Grand Prix und deren Strecken (nur Name) aus.*

.. code-block:: sql

   SELECT r.year, gp.name AS gp_name, c.name AS circuit_name
   FROM race r
   INNER JOIN grand_prix gp ON r.grand_prix_id = gp.id
   INNER JOIN circuit c ON r.circuit_id = c.id;

Aufgabe 3 - Sortierung
----------------------
*Aufgabe: Ordnen Sie die Rennen nach Jahr und benennen Sie die Spalten um.*

.. code-block:: sql

   SELECT r.year AS 'Saison', gp.name AS 'Grand Prix', c.name AS 'Strecke'
   FROM race r
   INNER JOIN grand_prix gp ON r.grand_prix_id = gp.id
   INNER JOIN circuit c ON r.circuit_id = c.id
   ORDER BY r.year ASC;

Aufgabe 4 - Theoriefrage
------------------------
*Frage: Macht es für Aufgabe 3 einen Unterschied, ob INNER JOIN oder LEFT JOIN verwendet wird?*

**Antwort:** In der vorliegenden F1-Datenbank macht es keinen Unterschied.
**Begründung:** Die referenzielle Integrität stellt sicher, dass jedes Rennen (`race`) zwingend einem Grand Prix und einer Strecke zugeordnet ist. Ein `LEFT JOIN` würde nur dann mehr Zeilen liefern, wenn es Rennen gäbe, die keine zugeordnete Strecke haben – was laut Datenmodell nicht erlaubt ist.

Aufgabe 5 – Keine doppelten Datensätze
--------------------------------------
*Aufgabe: Geben Sie alle Rennen und deren Strecken aus, ohne Duplikate.*

.. code-block:: sql

   SELECT DISTINCT gp.name, c.name
   FROM race r
   INNER JOIN grand_prix gp ON r.grand_prix_id = gp.id
   INNER JOIN circuit c ON r.circuit_id = c.id;

Aufgabe 6 – Komplexe Joins
--------------------------
*Aufgabe: Rennen, Teams und Punkte > 40 im Jahr 2014, sortiert nach Punkten.*

.. code-block:: sql

   SELECT gp.name AS race_name, con.name AS team_name, rcs.points
   FROM race_constructor_standing rcs
   INNER JOIN race r ON rcs.race_id = r.id
   INNER JOIN grand_prix gp ON r.grand_prix_id = gp.id
   INNER JOIN constructor con ON rcs.constructor_id = con.id
   WHERE r.year = 2014 AND rcs.points > 40
   ORDER BY rcs.points DESC;

Aufgaben zu Datenanpassungen
============================

Aufgabe 9 – Anpassen
--------------------
*Aufgabe: Benennen Sie das Team 'First' um in 'Last'.*

.. code-block:: sql

   UPDATE constructor
   SET name = 'Last'
   WHERE name = 'First';

Aufgabe 10 – Anpassen (CONCAT & CAST)
-------------------------------------
*Aufgabe: Hängen Sie die Anzahl Kurven (Turns) in Klammern an den Streckennamen an.*

.. code-block:: sql

   UPDATE circuit
   SET name = CONCAT(name, ' (', CAST(turns AS CHAR), ')');

Aufgabe 11 – Löschen
--------------------
*Aufgabe: Entfernen Sie alle Rundenzeiten (race_data) von Rennen mit Id < 500.*

.. code-block:: sql

   DELETE FROM race_data
   WHERE race_id < 500;

Aufgaben zu Transaktionen
=========================

Aufgabe 13 – Sicheres Löschen mit Transaktion
---------------------------------------------
*Aufgabe: Löschen eines Grand Prix (ID 960) inklusive aller Abhängigkeiten.*

.. code-block:: sql

   SET AUTOCOMMIT = 0;
   START TRANSACTION;

   # 1. Zuerst abhängige Kind-Datensätze löschen
   DELETE FROM race_data WHERE race_id = 960;
   DELETE FROM race_constructor_standing WHERE race_id = 960;
   DELETE FROM race_driver_standing WHERE race_id = 960;

   # 2. Dann den Eltern-Datensatz (Rennen) löschen
   DELETE FROM race WHERE id = 960;

   # Kontrolle: SELECT count(*) FROM race WHERE id = 960;
   COMMIT;

Aufgabe 14 – Sicheres Einfügen (MAX ID + 1)
-------------------------------------------
*Aufgabe: Neues Rennen 2029 anlegen unter Verwendung einer Variable.*

.. code-block:: sql

   SET AUTOCOMMIT = 0;
   START TRANSACTION;

   # Nächste ID berechnen und speichern
   SET @next_id = (SELECT MAX(id) + 1 FROM race);

   # Rennen einfügen
   INSERT INTO race (id, year, round, circuit_id, grand_prix_id, date, official_name)
   VALUES (@next_id, 2029, 1, 1, 1, '2029-05-20', 'Test Race 2029');

   # Abhängige Daten mit der neuen ID einfügen
   INSERT INTO race_constructor_standing (race_id, constructor_id, points, position)
   VALUES (@next_id, 1, 25, 1);

   COMMIT;

Aufgabe 15 – Fehlerfall und ROLLBACK
------------------------------------
*Aufgabe: Transaktion starten, Fehler provozieren und Rollback nachweisen.*

.. code-block:: sql

   START TRANSACTION;

   # 1. Gültiger Insert
   INSERT INTO race (id, year, round, circuit_id, grand_prix_id, date, official_name)
   VALUES (8888, 2030, 1, 1, 1, '2030-01-01', 'Rollback-Test');

   # 2. Fehler provozieren (FK-Verletzung: Konstruktor 99999 existiert nicht)
   INSERT INTO race_constructor_standing (race_id, constructor_id, points)
   VALUES (8888, 99999, 10);

   # Da der zweite Befehl fehlschlägt, machen wir alles rückgängig
   ROLLBACK;

   # Nachweis: SELECT * FROM race WHERE id = 8888; (Ergebnis muss leer sein)