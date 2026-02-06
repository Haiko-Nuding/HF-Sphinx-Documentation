ELK Troubleshooting: Fehlende Indizes beheben
=============================================

Wenn der Befehl ``sudo filebeat test output`` ein "OK" liefert, aber unter ``http://192.168.110.60:9200/_cat/indices?v`` keine Indizes erscheinen, folgen Sie diesen Schritten.

Symptom-Check
-------------

* **Verbindung:** OK (getestet via curl oder filebeat test).
* **Dienst:** Filebeat läuft auf dem Kali.
* **Problem:** Die Liste der Indizes zeigt nur interne Kibana-Einträge, aber kein ``filebeat-*``.

Schritt 1: Index-Templates manuell laden
----------------------------------------

Elasticsearch benötigt einen "Bauplan" (Template), um die Daten von Filebeat zu akzeptieren. Wenn dieser fehlt, werden Daten oft verworfen.

Führen Sie auf dem **Kali** aus:

.. code-block:: bash

   # Lädt Dashboards und Index-Templates auf die LM1
   sudo filebeat setup -e



Schritt 2: Berechtigungen und rsyslog prüfen
--------------------------------------------

Filebeat kann nur senden, was es lesen kann. Stellen Sie sicher, dass die Log-Datei existiert und lesbar ist.

.. code-block:: bash

   # Sicherstellen, dass rsyslog die Datei schreibt
   sudo systemctl restart rsyslog

   # Leserechte für Filebeat setzen
   sudo chmod 644 /var/log/auth.log

Schritt 3: Filebeat Registry Reset (Daten-Erzwingung)
-----------------------------------------------------

Filebeat merkt sich, bis zu welcher Zeile es eine Datei gelesen hat. Um Filebeat zu zwingen, die gesamte ``auth.log`` von vorne zu senden, muss die Registry gelöscht werden.

.. code-block:: bash

   # 1. Dienst stoppen
   sudo systemctl stop filebeat

   # 2. Lesestatus löschen
   sudo rm -rf /var/lib/filebeat/registry

   # 3. Dienst starten
   sudo systemctl start filebeat

Schritt 4: Manuelle Test-Daten generieren
-----------------------------------------

Filebeat reagiert oft erst, wenn sich die Datei ändert. Generieren Sie künstliche Fehlversuche direkt im Terminal:

.. code-block:: bash

   # Erzeugt 5 sofortige fehlgeschlagene Login-Einträge
   for i in {1..5}; do logger -t sshd "Failed password for root from 127.0.0.1 port 1234 ssh2"; done

   # Manueller Versuch via su
   su -c "ls" unbekannter_user

Schritt 5: Live-Analyse (Debug Mode)
------------------------------------

Wenn immer noch kein Index erscheint, starten Sie Filebeat im Vordergrund. Dies zeigt Ihnen in Echtzeit, ob Events versendet werden (``PublishEvents: X events have been published``).

.. code-block:: bash

   # Filebeat im Vordergrund mit Debug-Output starten
   sudo filebeat -e -v



Erfolgskontrolle
----------------

Aktualisieren Sie die Browserseite auf der LM1:

.. code-block:: text

   http://192.168.110.60:9200/_cat/indices?v

Sobald eine Zeile mit ``filebeat-8.10.2-...`` erscheint, war die Fehlerbehebung erfolgreich.