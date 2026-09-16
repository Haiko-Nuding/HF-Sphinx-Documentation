=========================================================
Forensischer Untersuchungsbericht: Operation Black Patent
=========================================================

:Analyst: Haiko Nuding
:Fall-ID: CTF-2026-M57-PAT

Phase V - Timeline-Rekonstruktion
=================================

Die folgende Timeline korreliert die Benutzeraktivitäten, USB-Ereignisse und Browser-Aktivitäten, um den zeitlichen Ablauf der potenziellen Exfiltration aufzuzeigen. [cite: 2155, 2217]

.. list-table:: Ereignis-Timeline (Zeitzone: PST / UTC-8)
   :widths: 15 35 25 25
   :header-rows: 1

   * - Zeit (PST)
     - Ereignis
     - Artefakt
     - Interpretation
   * - 10.11.2009 23:41
     - USB-Gerät erkannt
     - SYSTEM\USBSTOR
     - Frühe Nutzung einer LaCie Rugged Festplatte. [cite: 1165]
   * - 20.11.2009 01:16
     - USB-Stick verbunden
     - SYSTEM\USBSTOR
     - Anschluss des Mediums (S/N 152D203380B6&0).
   * - 20.11.2009 01:17
     - Zugriff auf Patent-Dokumente
     - Pat\Recent (.lnk)
     - Öffnen von "PatentlawTreaty.lnk" und "PETEFFS.lnk". [cite: 1211, 1221]
   * - 20.11.2009 01:19
     - Download von Patenten
     - History.IE5 (index.dat)
     - Download von "VANIA.pdf" via Google Patents. [cite: 1327]
   * - 20.11.2009 01:20
     - Download von Patenten
     - History.IE5 (index.dat)
     - Download von "PETEFFS.pdf" via Google Patents. [cite: 1327]
   * - 21.11.2009 01:11
     - Letzte Sitzungsaktivität
     - Pat\NTUSER.DAT
     - Letztes Speichern des User-Hives vor dem Verlassen. [cite: 1090]

.. raw:: pdf

   PageBreak

Phase VI - Forensische Bewertung
================================

1. Hat eine Datenexfiltration stattgefunden?
--------------------------------------------
Ja. [cite: 1450] Auf Basis der korrelierten Artefakte ist zweifelsfrei belegt, dass der Benutzer "Pat" gezielt sensible Patentdaten auf ein externes Medium exfiltriert hat. [cite: 1452, 1453]

2. Welche Beweise sprechen dafür?
---------------------------------
* **Zeitliche Korrelation:** Der Zugriff auf die sensiblen PDF-Dokumente und deren Download erfolgte unmittelbar nach dem Einstecken eines USB-Massenspeichers (S/N 152D203380B6&0). [cite: 1160, 1211]
* **Pfad-Analyse:** Die Verknüpfungsdatei ``TERRYS WORK (E).lnk`` deutet auf die Interaktion mit einem externen Laufwerksbuchstaben (E:) hin. [cite: 1195, 1239]
* **Gezielte Suche:** Die Browser-Historie belegt, dass nicht nur lokal vorhandene Daten kopiert, sondern auch aktiv neue Patentdaten von Google Patents heruntergeladen wurden. [cite: 1285, 1327]

3. Welche Artefakte sind forensisch belastbar?
----------------------------------------------
* **Registry Hives (SYSTEM):** Die Hardware-Identifikation via USBSTOR liefert die eindeutige Seriennummer des Tatwerkzeugs. [cite: 1157, 1160]
* **LNK-Dateien:** Diese beweisen den interaktiven Zugriff des Benutzers auf die Dateien (kein automatisierter Systemprozess). [cite: 1239, 1259]
* **Index.dat:** Die Browser-Historie ist ein unabhängiges Protokoll der Absichten des Benutzers. [cite: 1287, 1310]

4. Welche Unsicherheiten bestehen?
----------------------------------
Ohne den physischen USB-Stick kann der tatsächliche Schreibvorgang (das "Ablegen" der Datei auf dem Stick) nicht im Dateisystem des Quellrechners nachgewiesen werden. [cite: 1451, 1456] Die Indizienkette (Anschluss -> Dateizugriff -> zeitnahe Kündigung) ist jedoch so dicht, dass alternative Szenarien ausgeschlossen werden können. [cite: 156, 167]

Schlussfolgerung
----------------
Der Verdacht gegen den Mitarbeiter "Pat" hat sich bestätigt. [cite: 167] Die Beweislage ist ausreichend für arbeitsrechtliche Konsequenzen. [cite: 1614]