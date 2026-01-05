.. |logo| image:: ../_static/img/TofuBox_out.png
            :width: 40
            :alt: TofuBox Logo

|logo| TofuBox - Technische Dokumentation
=========================================================

.. meta::
   :description: Technische Dokumentation für das TofuBox HomeLab Projekt
   :keywords: Docker, MediaStack, Monitoring, ELK, Prometheus

:Projekt: TofuBox
:Team: Loris, Marc, Haiko
:Status: In Entwicklung
:Datum: 02.01.2025

.. only:: latex

    .. image:: ../_static/img/tofubox-web-qrcode.png
       :alt: TofuBox-Web-Doc
       :align: center
       :width: 50%

.. only:: html

    :download:`Download TofuBox - Technische Dokumentation <../_static/pdf/tofu_box_technische_documentation.pdf>`

    :download:`Download TofuBox Logo <../_static/img/resized_16x9_image_TofuBox_out.png>`

.. raw:: pdf

   PageBreak

.. raw:: pdf

   PageBreak

Einführung
==========

**TofuBox** ist ein umfassendes HomeLab-Projekt zur Bereitstellung und Überwachung von Mediendiensten. Das Herzstück bildet ein **Jellyfin**-Server zur Bereitstellung von Filmen und Serien, ergänzt durch einen vollautomatisierten "Arr-Stack" und ein professionelles Monitoring-System.

Projektstruktur
---------------

Das Projekt ist in verschiedene Docker-Stacks unterteilt, um eine modulare Wartung zu ermöglichen:

* **MediaStack**: Automatisierung von Downloads und Medienverwaltung.
* **Monitoring**: Überwachung der Systemressourcen und Dienste (Prometheus/Grafana).
* **Logging**: Zentralisierte Log-Analyse (ELK-Stack).
* **Collaboration**: Teaminterne Kommunikation via Mattermost.


Infrastruktur & Deployment
==========================

Docker Compose Konfiguration
----------------------------

Die folgende Konfiguration beschreibt den Kern des Monitoring- und Logging-Stacks.

.. code-block:: yaml
   :linenos:
   :caption: docker-compose.yml

   version: '3.9'

   services:
     # --- Monitoring (Prometheus & Grafana) ---
     monitor:
       image: prom/node-exporter:latest
       ports:
         - "9100:9100"

     prometheus:
       image: prom/prometheus:latest
       ports:
         - "9090:9090"
       volumes:
         - ./prom/prometheus.yml:/etc/prometheus/prometheus.yml:ro
         - promdata:/prometheus
       depends_on:
         - monitor

     grafana:
       image: grafana/grafana:latest
       ports:
         - "3000:3000"
       volumes:
         - grafanadata:/var/lib/grafana
       depends_on:
         - prometheus

     blackbox:
       image: prom/blackbox-exporter:latest
       ports:
         - "9115:9115"

     # --- Logging (ELK Stack) ---
     elasticsearch:
       image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
       container_name: elasticsearch
       environment:
         - discovery.type=single-node
         - xpack.security.enabled=false
         - ES_JAVA_OPTS=-Xms1g -Xmx1g
       ulimits:
         memlock:
           soft: -1
           hard: -1
       volumes:
         - esdata:/usr/share/elasticsearch/data
       ports:
         - "9200:9200"

     kibana:
       image: docker.elastic.co/kibana/kibana:8.15.0
       container_name: kibana
       depends_on:
         - elasticsearch
       environment:
         - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
       ports:
         - "5601:5601"

     logstash:
       image: docker.elastic.co/logstash/logstash:8.15.0
       container_name: logstash
       depends_on:
         - elasticsearch
       volumes:
         - ./logstash/pipeline:/usr/share/logstash/pipeline
       ports:
         - "5044:5044"

   volumes:
     dbdata:
     promdata:
     grafanadata:
     esdata:

.. raw:: pdf

   PageBreak

Mediastack (Ordner: /media)
===========================

Der Mediastack basiert auf dem "Arr-Framework" und nutzt **Gluetun** als VPN-Gateway für sichere Verbindungen.

Installation
------------

1. **Umgebungsvariablen**: Beispiel kopieren und anpassen:

   .. code-block:: bash

      cp .env.example .env

2. **Dienste starten**:

   .. code-block:: bash

      docker compose up -d

Komponenten
-----------

qBittorrent
^^^^^^^^^^^
Nach dem Start muss das temporäre Passwort aus den Logs ausgelesen werden:

.. code-block:: bash

   docker compose logs qbittorrent

.. important::
   In der WebUI (Port 8080) muss die Option **"Bypass authentication for clients on localhost"** aktiviert werden, damit das automatische Portforwarding von Gluetun funktioniert.

Gluetun
^^^^^^^
Verantwortlich für die VPN-Verbindung (OpenVPN). Zugangsdaten müssen in der ``.env`` hinterlegt sein.

Prowlarr / Radarr / Sonarr
^^^^^^^^^^^^^^^^^^^^^^^^^^
* **Prowlarr**: Indexer-Management.
* **Radarr**: Filme (Port 7878).
* **Sonarr**: Serien (Port 8989).

.. note::
   Bei der Verwendung von Gluetun muss in Radarr/Sonarr als Hostname für den Download-Client ``gluetun`` eingetragen werden.

.. raw:: pdf

   PageBreak

Collaboration & Messaging
=========================

Für Team-Alerts und Kommunikation nutzen wir **Mattermost**.

Setup Anforderungen
-------------------
Bevor der Stack gestartet wird, müssen Verzeichnisse und Berechtigungen manuell gesetzt werden:

.. code-block:: bash

   sudo mkdir -p config data logs
   sudo touch config/config.json
   sudo chown -R 2000:2000 config data logs


Monitoring & Analyse
====================


Das Monitoring-Konzept der TofuBox umfasst drei Ebenen:

1. **System-Metriken**: Node Exporter liefert CPU/RAM Auslastung an Prometheus.
2. **Service-Verfügbarkeit**: Blackbox Exporter prüft HTTP-Endpoints.
3. **Log-Analyse**: Der ELK-Stack (Elasticsearch, Logstash, Kibana) sammelt Container-Logs zur Fehlersuche.

Offene Punkte (Todo)
====================

* [ ] Vergleich: ``jellyfin/jellyfin`` vs ``linuxserver/jellyfin``.
* [ ] Dokumentation für Media-Folder Mapping vervollständigen.
* [ ] Dashboards in Grafana finalisieren.