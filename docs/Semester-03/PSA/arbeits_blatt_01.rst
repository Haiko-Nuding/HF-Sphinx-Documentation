=====================================================
Arbeitsblatt: Vorbereitung der Lernumgebung (Ansible)
=====================================================

Einleitung: Der Sinn der Automatisierung
----------------------------------------
In diesem Modul bauen wir eine **Infrastruktur als Code (IaC)** auf. Anstatt jeden Server einzeln zu konfigurieren (was bei 100 Servern unmöglich wäre), schreiben wir ein "Rezept" (das Playbook).

**Was passiert im Hintergrund?**
Wenn Sie den Befehl ``ansible-playbook`` ausführen, wird Ihr Admin-PC zur Kommandozentrale. Er loggt sich auf allen Servern gleichzeitig ein, installiert Programme und kopiert Dateien. Das Ziel ist eine **standardisierte Lernumgebung**, in der jeder Server exakt die gleiche Softwarebasis hat.

.. note::
   **Was ist Ansible?**
   Ein Werkzeug, das Befehle für Sie automatisiert. Anstatt 10-mal ``apt install docker`` auf verschiedenen Servern zu tippen, sagen Sie Ansible einmal: "Sorge dafür, dass Docker überall installiert ist."

Ziele
-----
* **Konnektivität:** Eine sichere "Vertrauensstellung" (SSH) zwischen Admin-PC und Servern aufbauen.
* **Provisionierung:** Automatische Installation von Docker, Git und Webdiensten.
* **Entwicklung:** Einrichten der PyCharm IDE für spätere Python-Projekte.

1. Das Fundament: SSH-Key-Authentifizierung
-------------------------------------------
**Warum machen wir das?** Ansible muss sich hunderte Male auf Servern einloggen. Würden wir Passwörter nutzen, müssten wir diese ständig tippen oder unsicher im Klartext speichern. **SSH-Keys** funktionieren wie ein digitaler Ausweis: Der Server erkennt Ihren Admin-PC automatisch wieder.



**Schritte:**

1. Öffnen Sie das Kali-Terminal via WSL:

   .. code-block:: bash

      wsl

2. Erstellen Sie Ihr digitales Schlüsselpaar:

   .. code-block:: bash

      ssh-keygen -t ed25519

3. Verteilen Sie Ihre "Visitenkarte" (Public Key) an die Server:
   *(Dies erlaubt Ihrem Admin-PC den Zugriff ohne Passwort-Abfrage.)*

   .. code-block:: bash

      ssh-copy-id vmadmin@192.168.110.10
      ssh-copy-id vmadmin@192.168.110.11
      ssh-copy-id vmadmin@192.168.110.12

2. Die Schaltzentrale: Ansible Konfiguration
--------------------------------------------
Wir erstellen nun die Baupläne für unsere Infrastruktur.

Die Bestandsaufnahme (Inventory)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Warum?** Ansible muss wissen, wer die Zielgeräte sind und welche individuellen Daten sie haben.
Die Datei ``hosts.ini`` definiert die "Rollen".

.. code-block:: ini

   [nodes]
   server-1 ansible_host=192.168.110.10 git_repo_url=https://github.com/GIBB-PSA/server-1.git
   server-2 ansible_host=192.168.110.11 git_repo_url=https://github.com/GIBB-PSA/server-2.git
   server-3 ansible_host=192.168.110.12 git_repo_url=https://github.com/GIBB-PSA/server-3.git

   [nodes:vars]
   ansible_user=vmadmin

.. note::
   **Der Sinn der Variablen:** Mit ``git_repo_url`` geben wir jedem Server ein individuelles Paket mit (z.B. bekommt Server-1 den Python-MQTT-Agenten, während Server-3 vielleicht eine Datenbank bekommt).

Das Playbook (Das Rezept)
~~~~~~~~~~~~~~~~~~~~~~~~~
**Warum?** Hier definieren wir den "Soll-Zustand". Es ist egal, wie der Server aktuell aussieht – nach dem Playbook wird er genau so konfiguriert sein, wie hier beschrieben.

.. code-block:: yaml

   - name: Setup GIBB-PSA Lernumgebung
     hosts: nodes
     become: yes  # Führt Befehle als Administrator (root) aus
     tasks:
       - name: Software-Basis installieren
         # Installiert Docker für Container und Git für den Code-Abruf
         apt:
           name: [git, docker.io, docker-compose]
           state: present
           update_cache: yes

       - name: Projekt-Ordner vorbereiten
         file:
           path: /opt/gibb_project
           state: directory
           owner: vmadmin

       - name: Code von GitHub beziehen
         # Nutzt die Variable aus der hosts.ini, um den richtigen Code zu laden
         git:
           repo: "{{ git_repo_url }}"
           dest: /opt/gibb_project

       - name: Docker-Webserver starten
         # Startet einen Nginx-Container, damit der Server über den Browser erreichbar ist
         shell: "docker-compose up -d"
         args:
           chdir: /opt/gibb_project



3. Ausführung: Die Automatisierung zünden
-----------------------------------------
Jetzt führen wir alles zusammen.

1. **Der Ping-Test:** Prüfen, ob die "Leitungen" (SSH) stehen.

   .. code-block:: bash

      ansible nodes -m ping -i hosts.ini

2. **Der Rollout:** Die gesamte Infrastruktur auf einmal aufbauen.

   .. code-block:: bash

      ansible-playbook -i hosts.ini setup_env.yml

**Was ist das Ergebnis?**
Nach dem Durchlauf sind alle Server provisioniert. Auf Server-1 läuft nun Ihr Python-Agent, auf Server-3 vielleicht eine Sicherheits-App (DVWA). Sie haben eine funktionierende Netzwerk-Umgebung geschaffen, ohne einen einzigen Server manuell konfigurieren zu müssen.