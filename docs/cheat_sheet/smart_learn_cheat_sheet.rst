========================================================================================================================
Smart-Learn Network, Service & Tooling Cheat Sheet
========================================================================================================================

Netzwerk-Konfiguration (Netplan & DNS)
======================================

Befehle für die statische IP-Konfiguration auf den Servern und DNS-Fixes auf dem Kali-Host.

Netplan auf dem Server anwenden:

.. code-block:: bash

    sudo netplan apply

DNS-Konfiguration der Nameserver prüfen:

.. code-block:: bash

    cat /etc/resolv.conf

DNS-Konfiguration manuell bearbeiten:

.. code-block:: bash

    sudo nano /etc/resolv.conf

Nameserver-Eintrag für Google DNS hinzufügen:

.. code-block:: bash

    nameserver 8.8.8.8

Internet-Erreichbarkeit via Domain testen:

.. code-block:: bash

    ping -c 4 google.ch

Internet-Erreichbarkeit via IP testen:

.. code-block:: bash

    ping -c 4 8.8.8.8

------------------------------------------------------------------------------------------------------------------------

Interface & Service Management
==============================

Befehle zum Zurücksetzen von Netzwerkkomponenten und Starten von Basis-Diensten auf dem System.

Netzwerk-Schnittstelle eth0 deaktivieren:

.. code-block:: bash

    sudo ifconfig eth0 down

Netzwerk-Schnittstelle eth0 aktivieren:

.. code-block:: bash

    sudo ifconfig eth0 up

Netzwerk-Manager Dienst komplett neu starten:

.. code-block:: bash

    sudo systemctl restart NetworkManager

SSH-Server für Remote-Zugriff manuell starten:

.. code-block:: bash

    sudo systemctl start ssh

------------------------------------------------------------------------------------------------------------------------

Software-Installation & Umgebung (Snap & Ansible)
=================================================

Einrichtung von Snap für GUI-Applikationen und Installation der Automatisierungs-Tools auf Kali.

Paketquellen aktualisieren und Snapd installieren:

.. code-block:: bash

    sudo apt update && sudo apt install snapd

Snap-Kommunikations-Socket aktivieren:

.. code-block:: bash

    sudo systemctl enable --now snapd.socket

Symlink für klassische Snap-Unterstützung erstellen:

.. code-block:: bash

    sudo ln -s /var/lib/snapd/snap /snap

PyCharm IDE im klassischen Modus installieren:

.. code-block:: bash

    sudo snap install pycharm --classic

PyCharm über den Snap-Pfad ausführen:

.. code-block:: bash

    /snap/bin/pycharm

Ansible Automatisierungs-Software installieren:

.. code-block:: bash

    sudo apt install ansible -y

------------------------------------------------------------------------------------------------------------------------

Remote-Checks & Sicherheitsscan
===============================

Überprüfung von Remote-Konfigurationen und Port-Scans mit Nmap für Sicherheitsanalysen.

Inhalt der Remote-Service-Datei anzeigen (SSH-Abfrage):

.. code-block:: bash

    ssh vmadmin@192.168.110.10 "cat /etc/systemd/system/socket_server.service"

Nmap-Scan mit Versionserkennung auf Ziel-IP ausführen:

.. code-block:: bash

    sudo nmap -p 1883,3000,8080,2121,2222 -sV 192.168.110.12

Nmap-Scan mit Stealth-Technik (TCP NULL Scan):

.. code-block:: bash

    sudo nmap -sN 192.168.110.12

------------------------------------------------------------------------------------------------------------------------

Fehlersuche (Quick-Troubleshooting)
===================================

Wichtige Prüfschritte bei Verbindungsproblemen.

Status des Snap-Dienstes abfragen:

.. code-block:: bash

    systemctl status snapd.socket

Netzwerk-Schnittstellen und IP-Adressen anzeigen:

.. code-block:: bash

    ifconfig

Routing-Tabelle und Default Gateway prüfen:

.. code-block:: bash

    ip route show