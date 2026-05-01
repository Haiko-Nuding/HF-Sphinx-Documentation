===================================
MSA I - Prüfungs-Spickzettel
===================================

Netzwerk-Diagnose (Win+R / CMD)
-------------------------------

Netzwerkadapter-Einstellungen öffnen
.. code-block:: bash

   ncpa.cpl

Vollständige IP-Konfiguration anzeigen
.. code-block:: bash

   ipconfig /all

DNS-Cache leeren
.. code-block:: bash

   ipconfig /flushdns

DNS-Einträge am Server aktualisieren
.. code-block:: bash

   ipconfig /registerdns

Namensauflösung eines Hosts testen
.. code-block:: bash

   nslookup <Ziel>

Verbindung/Erreichbarkeit prüfen
.. code-block:: bash

   ping <IP/Hostname>

System & Tools (Win+R)
----------------------

Computerverwaltung (Alles-in-Einem)
.. code-block:: bash

   compmgmt.msc

Dienste verwalten
.. code-block:: bash

   services.msc

Task-Manager (Prozesse/Auslastung)
.. code-block:: bash

   taskmgr

Ereignisanzeige (Fehler-Logs lesen)
.. code-block:: bash

   eventvwr

Systemeigenschaften (Domänenbeitritt)
.. code-block:: bash

   sysdm.cpl

Klassische Systemsteuerung öffnen
.. code-block:: bash

   control

Festplatten-Partitionierung (CMD)
.. code-block:: bash

   diskpart

Server-Verwaltung (Win+R)
-------------------------

Active Directory Benutzer & Computer
.. code-block:: bash

   dsa.msc

Gruppenrichtlinien-Verwaltung (GPO)
.. code-block:: bash

   gpmc.msc

DNS-Manager
.. code-block:: bash

   dnsmgmt.msc

DHCP-Konsole
.. code-block:: bash

   dhcpmgmt.msc

Server-Manager (Rollen-Installation)
.. code-block:: bash

   servermanager

Performance-Überwachung
.. code-block:: bash

   perfmon

Ressourcenmonitor
.. code-block:: bash

   resmon

Server & GPO (CMD/PowerShell)
-----------------------------

FSMO-Rollen-Master anzeigen
.. code-block:: bash

   netdom query fsmo

Angewendete GPOs für User/Computer prüfen
.. code-block:: bash

   gpresult /r

GPO-Richtlinien sofort neu erzwingen
.. code-block:: bash

   gpupdate /force

PowerShell (Admin-Konsole)
--------------------------

RSAT-Tools finden
.. code-block:: powershell

   Get-WindowsCapability -Name RSAT* -Online

Alle gestoppten Dienste auflisten
.. code-block:: powershell

   Get-Service | Where-Object {$_.Status -eq 'Stopped'}

Systemdateien auf Fehler prüfen
.. code-block:: powershell

   sfc /scannow