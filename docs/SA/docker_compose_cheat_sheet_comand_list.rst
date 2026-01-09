Docker Compose Cheat Sheet (Befehlsliste)
=========================================

Diese Liste enthält die wichtigsten Befehle für die tägliche Arbeit mit Docker Compose.
Alle Befehle müssen im Verzeichnis der ``docker-compose.yaml`` ausgeführt werden.

Die wichtigsten Lifecycle-Befehle
---------------------------------

**Container im Hintergrund starten:**

.. code-block:: bash

   docker-compose up -d

**Alle Container stoppen und entfernen:**

.. code-block:: bash

   docker-compose down

**Container stoppen und auch alle Daten (Volumes) löschen:**

.. code-block:: bash

   docker-compose down -v

**Container nur stoppen (bleiben vorhanden):**

.. code-block:: bash

   docker-compose stop

**Container wieder starten:**

.. code-block:: bash

   docker-compose start

Monitoring & Fehlersuche
------------------------

**Status aller Container anzeigen:**

.. code-block:: bash

   docker-compose ps

**Live-Logs aller Services anzeigen:**

.. code-block:: bash

   docker-compose logs -f

**Live-Logs eines spezifischen Services (z.B. "db"):**

.. code-block:: bash

   docker-compose logs -f db

**Die aktuelle Konfiguration prüfen (Syntax-Check):**

.. code-block:: bash

   docker-compose config

Interaktion & Wartung
---------------------

**Befehl im laufenden Container ausführen (Shell öffnen):**

.. code-block:: bash

   docker-compose exec web sh

**Einen einzelnen Service neu starten:**

.. code-block:: bash

   docker-compose restart api

**Image-Updates herunterladen:**

.. code-block:: bash

   docker-compose pull

**Images neu bauen (nach Änderungen am Dockerfile):**

.. code-block:: bash

   docker-compose build

Fortgeschrittene Nutzung
------------------------

**Befehl mit einer spezifischen Datei ausführen:**

.. code-block:: bash

   docker-compose -f production.yaml up -d

**Ressourcenverbrauch der Container anzeigen:**

.. code-block:: bash

   docker-compose top