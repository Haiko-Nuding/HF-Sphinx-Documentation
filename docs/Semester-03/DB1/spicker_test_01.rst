Dieser Guide deckt den Workflow für die Arbeitsblätter AB1 bis AB3 ab.
Hinweis: Werte in `< >` sind Platzhalter und müssen ersetzt werden.

----------------------------------------------------------
1. Einstieg & Datenbank-Setup (AB1)
----------------------------------------------------------

**Login & Verbindung:**

.. code-block:: batch

   # Login über die Windows CMD (Passwort wird danach abgefragt)
   mariadb -u root -p

**Datenbank innerhalb von MariaDB erstellen:**

.. code-block:: sql

   -- utf8mb4 stellt sicher, dass Umlaute/Sonderzeichen korrekt gespeichert werden
   CREATE DATABASE <datenbank_name> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   EXIT;

**Daten-Import & Export (Backup):**

.. code-block:: batch

   # IMPORT: SQL-Skript in eine bestehende Datenbank einspielen
   mariadb -u root -p <datenbank_name> < "C:\Pfad\zu\datei.sql"

   # EXPORT (DUMP): Backup einer Datenbank in eine Datei erstellen
   mariadb-dump -u root -p <datenbank_name> > "C:\Pfad\zu\backup_name.sql"

----------------------------------------------------------
2. Navigation im MariaDB Monitor
----------------------------------------------------------

**Datenbank & Tabellen erkunden:**

.. code-block:: sql

   SHOW DATABASES;      -- Alle verfügbaren DBs auflisten
   USE <datenbank_name>;-- In die Datenbank wechseln
   SHOW TABLES;         -- Tabellen der aktuellen DB anzeigen
   DESCRIBE <tabelle>;  -- Spalten, Datentypen und Keys (PK/FK) anzeigen

----------------------------------------------------------
3. Daten abfragen & Filtern (AB2)
----------------------------------------------------------

**Grundlagen & Aliase:**

.. code-block:: sql

   SELECT name FROM products;
   SELECT product_name AS "Fahrrad", list_price AS "Preis" FROM products;

**Gruppieren & Aggregatfunktionen (Reports):**

.. code-block:: sql

   -- GROUP BY: Daten nach einer Spalte zusammenfassen
   -- Beispiel: Wie viele Fahrräder gibt es pro Modelljahr?
   SELECT model_year, COUNT(*) AS "Anzahl_Bikes"
   FROM products
   GROUP BY model_year
   ORDER BY model_year DESC;

**Filtern & Mustersuche:**

.. code-block:: sql

   SELECT * FROM products WHERE list_price > 1000;
   SELECT * FROM products WHERE product_name LIKE 'Heller%';
   SELECT * FROM staffs WHERE manager_id IS NULL;  -- NULL finden (Felder ohne Eintrag)

----------------------------------------------------------
4. Joins & Datenänderungen (AB3)
----------------------------------------------------------

**Join-Übersicht & Logik:**

.. list-table:: JOIN-Arten im Überblick
   :widths: 20 40 40
   :header-rows: 1

   * - Join-Art
     - Logik (Interesse)
     - Praxis-Beispiel (BikeStore)
   * - **INNER JOIN**
     - Nur Treffer in BEIDEN Tabellen.
     - Produkte mit ihren Kategorien anzeigen.
   * - **LEFT JOIN**
     - Alles von Links, auch ohne Partner.
     - Kunden finden, die noch nie bestellt haben.
   * - **SELF JOIN**
     - Tabelle mit sich selbst verbinden.
     - Mitarbeiter ihrem Manager zuordnen.

.. raw:: pdf

   PageBreak

**Tabellen verbinden (JOINs):**

.. code-block:: sql

   -- INNER JOIN: Nur Zeilen mit Partner in beiden Tabellen (Schnittmenge)
   -- Beispiel: Welches Produkt gehört zu welcher Kategorie?
   SELECT p.product_name, c.category_name
   FROM products p
   INNER JOIN categories c ON p.category_id = c.category_id;

   -- LEFT JOIN: Alle Zeilen links, auch wenn rechts kein Partner existiert
   -- Beispiel: Finde Kunden (links), die noch nie bestellt haben (Lücken-Analyse)
   SELECT cu.first_name, cu.last_name, o.order_id
   FROM customers cu
   LEFT JOIN orders o ON cu.customer_id = o.customer_id
   WHERE o.order_id IS NULL;

   -- SELF JOIN: Tabelle mit sich selbst verbinden (Spezialfall)
   -- Beispiel: Name des Mitarbeiters und Name seines zugeordneten Managers
   SELECT m.first_name AS "Mitarbeiter", s.first_name AS "Manager"
   FROM staffs m
   LEFT JOIN staffs s ON m.manager_id = s.staff_id;

**Datenmanipulation (DML):**

.. code-block:: sql

   -- INSERT: Datensatz anlegen
   INSERT INTO categories (category_name) VALUES ('E-Bikes');

   -- UPDATE: Daten ändern (WICHTIG: WHERE nutzen!)
   UPDATE products SET list_price = list_price * 1.1 WHERE brand_id = 5;

   -- DELETE: Daten löschen (Reihenfolge: Kind-Tabelle vor Eltern-Tabelle)
   -- Zuerst Abhängigkeiten (FK) löschen, dann den Hauptdatensatz (PK)
   DELETE FROM stocks WHERE product_id = 100;
   DELETE FROM products WHERE product_id = 100;

5. Spezialfälle & Variablen
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Besonderheiten beim Dateneinfügen (Code-Beispiele):**

.. code-block:: sql

   -- IDENTITY / AUTO_INCREMENT:
   -- Wenn eine ID automatisch hochzählt, lässt man sie beim INSERT einfach weg.
   -- MariaDB vergibt dann automatisch die nächste freie Nummer.
   INSERT INTO stores (store_name, city) VALUES ('Bern Bikes', 'Bern');

   -- NULL zugelassen:
   -- Felder, die NULL erlauben, können beim INSERT ignoriert oder explizit geleert werden.
   -- Mit IS NULL prüft man auf leere Felder, mit = NULL setzt man sie.
   UPDATE customers SET phone = NULL WHERE customer_id = 10;
   SELECT * FROM customers WHERE phone IS NULL;

   -- Bulk Insert (Mehrere Zeilen gleichzeitig):
   -- Deutlich schneller als viele Einzel-Inserts. Wertepaare werden mit Komma getrennt.
   INSERT INTO brands (brand_name) VALUES ('Brand Alpha'), ('Brand Beta'), ('Brand Gamma');

**Manipulation & Variablen:**

.. code-block:: sql

   -- CONCAT: Strings zusammenfügen (Leerzeichen zwischen ' ' nicht vergessen!)
   SELECT CONCAT(first_name, ' ', last_name) AS full_name
   FROM staffs WHERE manager_id IS NULL;

   -- SET @variable: Wert für die aktuelle Session speichern (flüchtig!)
   -- WICHTIG: Variablen werden NICHT zwischen CLI und Workbench geteilt!
   SET @id_suche := (SELECT product_id FROM products WHERE product_name = 'Heller Shagamaw Frame - 2016');

   -- Variable in der gleichen Session kontrollieren
   SELECT @id_suche;


6. Transaktionen & Sicherheit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sicheres Arbeiten bei DELETE und UPDATE Befehlen (Aufgabe 13-15).

.. code-block:: sql

   SET AUTOCOMMIT = 0;  -- Automatisches Speichern AUS
   START TRANSACTION;   -- Sicherer Modus AN (Änderungen sind noch lokal)

   -- Beispiel: Kaskadierendes Löschen von Hand
   DELETE FROM order_items WHERE order_id = 960;
   DELETE FROM orders WHERE order_id = 960;

**Integritäts-Check vor dem COMMIT:**

.. code-block:: sql

   -- WICHTIG: Prüfen, wie viele Zeilen wirklich betroffen sind
   SELECT ROW_COUNT();

   -- Manueller Check: Ist die ID innerhalb der Session wirklich weg?
   SELECT COUNT(*) FROM orders WHERE order_id = 960;

   COMMIT;              -- Speichern (Dauerhaft auf Festplatte)
   ROLLBACK;            -- Abbruch (Alles rückgängig machen)