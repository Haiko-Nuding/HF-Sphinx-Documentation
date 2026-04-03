========================================================================================================================
Ansible Deployment Cheat Sheet
========================================================================================================================

Projekt-Architektur und Dateipfade
==================================

In einer Standard-Ansible-Struktur liegen die Dateien wie folgt im Projektverzeichnis:

.. code-block:: text

    socket_com/               <-- Projekt-Wurzelverzeichnis (Root)
    ├── ansible.cfg           # Konfiguration (immer im Root-Verzeichnis ablegen)
    ├── inventory.ini         # Host-Liste (Adressbuch der Ziel-Server)
    ├── deploy_server.yml     # Das Playbook (Enthält die Logik und alle Tasks)
    ├── secret.key            # Symmetrischer Schlüssel für die Fernet-Verschlüsselung
    └── templates/            # ORDNER für Jinja2-Vorlagen (z. B. Systemd-Units)
        └── socket_server.service.j2

------------------------------------------------------------------------------------------------------------------------

Kern-Komponenten im Detail
==========================

.. list-table:: Datei-Navigation und Zweck
   :widths: 25 35 60
   :header-rows: 1

   * - Komponente
     - Standard-Pfad
     - Beschreibung
   * - Konfiguration
     - ``./ansible.cfg``
     - Steuert das globale Verhalten (z. B. SSH-Agent Forwarding, Timeouts, Remote-User).
   * - Inventar
     - ``./inventory.ini``
     - Definiert das "Wo": Gruppiert IP-Adressen oder Hostnamen der Zielsysteme.
   * - Playbook
     - ``./deploy_server.yml``
     - Definiert das "Was": Die Abfolge der Tasks (Installation, Copy, Restart).
   * - Vorlagen
     - ``./templates/*.j2``
     - Dynamische Dateien, die zur Laufzeit mit Variablen auf den Server angepasst werden.

------------------------------------------------------------------------------------------------------------------------

Wichtige Befehle (CLI)
======================

Playbook ausführen:

.. code-block:: bash

    ansible-playbook -i inventory.ini deploy_server.yml

Verbindung zu allen Hosts im Inventory testen (Ping-Modul):

.. code-block:: bash

    ansible all -i inventory.ini -m ping

Syntax-Check für das Playbook durchführen:

.. code-block:: bash

    ansible-playbook -i inventory.ini deploy_server.yml --syntax-check

Dienststatus auf Remote-Servern direkt prüfen (Ad-hoc Befehl):

.. code-block:: bash

    ansible socket_servers -i inventory.ini -a "systemctl status socket_server"

------------------------------------------------------------------------------------------------------------------------

Lösungen für kritische Deployment-Herausforderungen
===================================================

SSH-Agent Forwarding
--------------------
Damit Git-Cloning von privaten Repos funktioniert, muss der lokale SSH-Key durchgereicht werden:

1. In der ``ansible.cfg`` muss ``ssh_args = -o ForwardAgent=yes`` konfiguriert sein.
2. Lokal auf dem Host muss der Key geladen sein (Prüfung via ``ssh-add -l``).

Systemd & Daemon-Reload
-----------------------
Wenn die Service-Datei (``.service.j2``) geändert wurde, muss Systemd die Konfiguration neu einlesen.
Im Playbook nutzen wir dafür im Modul ``ansible.builtin.systemd`` den Parameter ``daemon_reload: yes``.

Privilegiensteuerung (Become)
-----------------------------
* ``become: yes``: Erforderlich für System-Operationen (Root), wie APT-Installs oder Service-Verwaltung.
* ``become: no``: Wichtig für User-Operationen (vmadmin), wie Pip-Installs mit aktivem SSH-Forwarding.

------------------------------------------------------------------------------------------------------------------------

Best Practices für die Wartbarkeit
==================================

* Trenne die Logik (Playbook) strikt von den Daten (Variablen in group_vars).
* Nutze immer den Unterordner ``templates/``, da Ansible dort implizit nach Vorlagen sucht.
* Halte Zeilen konsequent unter 120 Zeichen, um die Lesbarkeit in Git-Diffs und IDEs zu optimieren.