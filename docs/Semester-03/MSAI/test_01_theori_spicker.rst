============================================
Ultimativer Theorie-Spicker: MSA I
============================================

1. Active Directory (AD DS) - Das Herzstück
============================================

Grundlagen & Struktur
---------------------

* **Struktur**: Forest (höchste Ebene, Schema-Container) -> Tree (Organisationseinheit) -> Objekte (User, Computer, Gruppen).
* **Domänencontroller (DC)**: Server, die die AD-Datenbank hosten und für Authentifizierung, Autorisierung und Replikation zuständig sind.
* **Global Catalog (GC)**: Spezielle Rolle eines DCs. Hält eine Teilkopie aller Objekte des Forests.
    * Notwendig für Forest-weite Suche.
    * Notwendig für Anmeldung bei Universal Groups (wichtig bei Multi-Domain-Umgebungen).
* **Vertrauensstellungen (Trusts)**: Ermöglichen Zugriff auf Ressourcen über Domänengrenzen hinweg.

FSMO-Rollen (Zuständigkeits-Matrix)
-----------------------------------

.. list-table:: FSMO-Rollen
   :widths: 20 20 60
   :header-rows: 1

   * - Rolle
     - Ebene
     - Funktion
   * - Schema Master
     - Forest
     - Einziges Objekt für Änderungen am AD-Schema (Definitionen)
   * - Domain Naming Master
     - Forest
     - Verwaltet Domänennamen und Namespaces
   * - RID Master
     - Domain
     - Vergibt SID-Pools an DCs für neue Objekterstellung
   * - PDC Emulator
     - Domain
     - Master für Passwort-Änderungen und Zeit-Synchronisation
   * - Infrastructure Master
     - Domain
     - Korrigiert Querverweise auf Objekte in anderen Domänen

**Hinweis zum Infrastructure Master**: Darf niemals auf einem DC liegen, der auch Global Catalog (GC) ist (außer in Single-Domain-Umgebungen), da der GC keine Updates von anderen Domänen erhält und der Infra-Master sonst veraltete Daten hält.

2. Netzwerk-Dienste (DNS & DHCP)
================================

DHCP (Dynamic Host Configuration Protocol) - DORA
-------------------------------------------------

1. **Discovery**: Client sendet Broadcast ("Wer ist DHCP?").
2. **Offer**: Server bietet IP an ("Ich bin da, hier ist eine IP").
3. **Request**: Client will die IP ("Ich nehme dein Angebot").
4. **Acknowledgement**: Server bestätigt ("IP ist reserviert/zugewiesen").

DNS (Domain Name System)
------------------------

* **Records**:
    * A: Name zu IPv4.
    * AAAA: Name zu IPv6.
    * CNAME: Alias (Verweis auf einen anderen Namen).
    * MX: Mailserver.
    * SRV: Service-Locator (wichtigster Record für AD, um DC-Dienste zu finden).
* **Zonen**:
    * Forward: Namensauflösung (Name -> IP).
    * Reverse: IP-Auflösung (IP -> Name).

3. Windows Architektur (Die "Hard-Theory")
==========================================

* **User Mode (Ring 3)**: Applikationen (Word, Browser). Kein direkter Hardware-Zugriff. Fehler führen zu App-Absturz, nicht zum OS-Absturz.
* **Kernel Mode (Ring 0)**: Hardwarezugriff, Treiber, OS-Kern. Fehler führen zum BSOD (Bluescreen).

Speicher-Management:
--------------------

* **Paged Pool**: Speicherbereiche, die auf die HDD/SSD (pagefile.sys) ausgelagert werden können.
* **Nonpaged Pool**: Muss IMMER im RAM bleiben.

.. raw:: pdf

   PageBreak

4. Glossar & Abkürzungen
========================

Active Directory & Verwaltung
-----------------------------
* **GPO (Group Policy Object):** Richtlinie zur zentralen Konfiguration.
* **RSAT (Remote Server Administration Tools):** Sammlung von Tools zur Remote-Administration von Servern.
* **SID (Security Identifier):** Eindeutige ID für jedes Objekt im Active Directory.

Netzwerk & Abläufe
------------------
* **DORA (DHCP Ablauf):** Die Prozessschritte Discovery, Offer, Request, Acknowledgement.
* **LSDOU (GPO-Reihenfolge):** Lokal -> Site -> Domain -> OU (OU gewinnt bei Widersprüchen).

System-Architektur & Sicherheit
-------------------------------
* **ACL (Access Control List):** Liste, die festlegt, wer welche Rechte auf eine Ressource hat.
* **BSOD (Blue Screen of Death):** Systemabsturz bei Kernel-Ring-Fehlern.
* **HAL (Hardware Abstraction Layer):** Zwischenschicht zwischen Kernel und physischer CPU/Hardware.
* **UAC (User Account Control):** Sicherheitsmechanismus, der Programme einschränkt, bis Admin-Rechte bestätigt werden.

Dateisysteme
------------
* **NTFS (New Technology File System):** Standard-Dateisystem (bietet Journaling, Berechtigungen).
* **ReFS (Resilient File System):** Dateisystem mit Fokus auf Stabilität/Integrität, kein Ersatz für Systemlaufwerke.

5. Wartung & Admin-Tools
========================

.. list-table:: Wartung & Tools
   :widths: 30 70
   :header-rows: 1

   * - Befehl/Tool
     - Einsatz/Zweck
   * - sfc /scannow
     - Prüft/repariert geschützte Windows-Systemdateien
   * - dism/restorehealth
     - Repariert das System-Image über Windows Update
   * - Shift + F10
     - Öffnet CMD während des Setups (Diskpart, Debugging)
   * - utilman.exe Hack
     - Umbenennen von utilman.exe in cmd.exe für Passwort-Reset
   * - services.msc
     - GUI-Verwaltung für Dienste (Hintergrundprogramme)
   * - WinGet
     - Paketmanager für CLI-Softwareinstallation

6. Typische Lehrer-Fallen (Prüfungs-Check)
===========================================

Active Directory & Domänen-Struktur
-----------------------------------

* **"Darf man den Infrastructure Master auf einen Global Catalog (GC) legen?"**
  Antwort: In Multi-Domain-Umgebungen auf keinen Fall! Der Infra-Master braucht Objektdaten, die nicht im Global Catalog stehen. Er würde sonst veraltete Daten halten.

* **"Darf man einen Domain Controller einfach per VM-Snapshot auf einen alten Stand zurücksetzen?"**
  Antwort: Auf keinen Fall! Dies führt zum "USN Rollback"-Problem. Die AD-Datenbanken korrumpieren, da die Replikations-IDs (USN) nicht mehr zu den anderen DCs passen.

* **"Was ist der Unterschied zwischen Forest und Tree?"**
  Antwort: Der Forest ist die höchste Ebene (enthält das Schema), ein Tree ist eine logische Gruppierung von Domänen innerhalb eines Forests.

GPO & Berechtigungs-Logik
-------------------------

* **"Was ist die GPO-Reihenfolge?"**
  Antwort: Immer **LSDOU** (Lokal, Site, Domain, OU). Die letzte Instanz (OU) hat das Sagen und überschreibt Widersprüche.

* **"Was passiert, wenn eine GPO 'erzwungen' (Enforced) wird?"**
  Antwort: Diese Einstellung überschreibt alle widersprüchlichen Einstellungen in untergeordneten OUs, selbst wenn dort eine 'Blockierung der Vererbung' konfiguriert ist.

* **"Welche Berechtigung gewinnt bei Freigaben und NTFS?"**
  Antwort: Immer die restriktivere (einschränkendere) Regel gewinnt.

* **"Was ist der Unterschied zwischen Computerkonfiguration und Benutzerkonfiguration?"**
  Antwort: Computerkonfiguration greift beim Systemstart (vor Login), Benutzerkonfiguration erst bei der Anmeldung des Users.



Netzwerk-Dienste (DNS & DHCP)
-----------------------------

* **"Client bekommt keine IP, was ist kaputt?"**
  Antwort: DHCP. (Zusatz: Prüfe, ob er eine APIPA-Adresse 169.254.x.x hat, um lokale Kommunikation zu ermöglichen).

* **"Client findet Server nicht per Name, was ist kaputt?"**
  Antwort: DNS (SRV-Records fehlen oder DNS-Auflösung defekt).

Windows-Systemarchitektur & Wartung
-----------------------------------

* **"Warum stürzt Word ab, aber das System nicht?"**
  Antwort: Isolation im User Mode (Ring 3). Fehler bleiben auf den Prozess beschränkt. Kernel Mode (Ring 0) Fehler korrumpieren den globalen Speicherzustand -> BSOD.

* **"Was ist der Unterschied zwischen FAT32 und NTFS?"**
  Antwort: FAT32 ist kompatibel (USB), NTFS bietet Sicherheit (ACLs, Journaling) und hat kein 4GB-Dateilimit.

* **"Wann nutze ich sfc und wann dism?"**
  Antwort: Erst sfc (Dateien prüfen). Wenn sfc beschädigte Dateien findet, die es nicht selbst reparieren kann, nutzt man dism (Image reparieren).

* **"Warum scheitert die Anmeldung von Usern, obwohl DC erreichbar ist?"**
  Antwort: Oft ist die Zeit-Synchronisation (über den PDC Emulator) fehlerhaft. Kerberos benötigt eine präzise Zeit (max. 5 Minuten Abweichung).