03_OffensiveSecurity
====================

Offensive Security als strukturiertes Analysemodell

Typische professionelle Struktur: 

1. Reconnaissance 
2. Initial Access 
3. Privilege Escalation 
4. Persistence 
5. Lateral Movement 
6. Impact 


Diese Struktur ist des Angreifers Denkmodell. 

In der Praxis Sind diese Phasen dynamisch. Ein Angreifer springt 
zwischen ihnen hin und her. 



1 Reconnaissance – Informationsgewinnung
----------------------------------------

Typische Werkzeuge: 

nmap -> (Network Mapper) Netzwerkerkennung / Portscanning
smtp-user-enum -> (CLI Tool) OSINT- Pentesting-Tool : Benutzernamen auf einem SMTP-Server identifizieren (Enumeration)
Netcat -> (Network Tool) Banner Grabbing : Auslesen von Dienst-Metadaten durch Port-Verbindungen (Information Gathering)
Metasploit Auxiliary -> (Modular Framework) Information Gathering / Scanning : Hilfsmodule zur Durchführung von Portscans, Service-Enumeration und Schwachstellen-Checks (ohne Payload).


2 Initial Access 
----------------


Das kann erfolgen durch: 

- Web Application Misconfiguration 
- CredentialAttacks 
- Exploit einer bekannten Schwachstelle 
- Standardpasswoerter 
- Social Engineering

Werkzeuge: 
- Metasploit Exploits -> (Attack Modules) Schwachstellenausnutzung : Code-Ausführung auf Zielsystemen (System-Compromise).
- Hydra -> (Login Cracker) Password-Auditing : Brute-Force gegen Anmeldedaten.
- Manuelle Protokollinteraktion -> (Direct Communication) Service-Testing : Direkte Befehlseingabe in Protokolle (SMTP, HTTP, POP3).

Wichtig: 
Initial Access bedeutet selten sofort root. 
Er bedeutet begrenzten Kontext. 