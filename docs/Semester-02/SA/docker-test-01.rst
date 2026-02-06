Mattermost Container Setup & Webhook Test
=========================================

Diese Anleitung führt durch die Installation von Docker, das Deployment von Mattermost auf der LM1 sowie den Test der Webhook-Schnittstelle.

Step 1: System vorbereiten (LM1)
--------------------------------

Zuerst aktualisieren wir die Paketquellen und installieren Docker.

.. code-block:: bash

   sudo apt update

.. code-block:: bash

   sudo apt install -y docker.io docker-compose-v2

Step 2: Berechtigungen korrigieren
----------------------------------

Um Docker ohne ``sudo`` zu nutzen und den "permission denied" Fehler zu beheben, fügen wir den User der Gruppe hinzu.

.. code-block:: bash

   sudo usermod -aG docker $USER

Wende die Gruppenänderung sofort an, ohne dich neu einzuloggen:

.. code-block:: bash

   newgrp docker

Step 3: Projektverzeichnis erstellen
------------------------------------

Wir erstellen den Ordner für die Konfigurationsdatei.

.. code-block:: bash

   mkdir -p ~/workstation/project-mattermost

.. code-block:: bash

   cd ~/workstation/project-mattermost

Step 4: Docker-Compose Datei erstellen
--------------------------------------

Erstellen Sie die Datei ``docker-compose.yaml`` (ohne die veraltete 'version' Zeile).

.. code-block:: yaml

   services:
     mattermost:
       image: mattermost/mattermost-preview
       container_name: mattermost
       restart: unless-stopped
       ports:
         - "8065:8065"

Step 5: Mattermost starten
--------------------------

Starten Sie den Container im Hintergrund.

.. code-block:: bash

   docker compose up -d

Step 6: Konfiguration im Web-GUI
--------------------------------

Öffnen Sie den Browser auf dem **Kali-System** und rufen Sie die Adresse der LM1 auf:

.. code-block:: text

   http://192.168.110.60:8065

**Schritte im GUI:**
1. Administrator-Konto erstellen.
2. Team mit dem Namen ``DevOps`` anlegen.
3. **Webhooks global erlauben:**
   * Gehe zu: **System Console** -> **Integrations** -> **Integration Management**.
   * Setze **Enable Incoming Webhooks** auf ``true``.
   * Klicke unten auf **Save**.
4. **Webhook erstellen:**
   * Gehe zu: **Main Menu** (oben links) -> **Integrations** -> **Incoming Webhooks**.
   * Klicke auf **Add Incoming Webhook**.
   * Name: ``Test-Hook``, Channel: ``Town Square``.
   * Speichere den Webhook und kopiere die generierte URL.

Step 7: HTTP Testnachricht senden
---------------------------------

Führen Sie diesen Befehl aus, um eine Testnachricht per HTTP POST an die LM1 zu senden. Ersetzen Sie ``<DEINE_URL>`` durch den kopierten Link.

.. code-block:: bash

   curl -i -X POST -H 'Content-Type: application/json' \
   -d '{"text": "HTTP POST Test: Mattermost läuft erfolgreich im Container auf LM1!"}' \
   <DEINE_URL>

**Erfolgskontrolle:**
In Mattermost sollte nun die Nachricht im Channel "Town Square" erscheinen.

.. note::
   Machen Sie einen Screenshot vom Terminal (nach dem curl Befehl) und vom Mattermost-Channel für die Abgabe.