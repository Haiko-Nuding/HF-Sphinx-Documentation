Main Übersicht Context
======================
Thema: Windows Server Administration (MSA) Lab
Zweck: Verwaltung von Active Directory Objekten (Benutzer & Computer)
Domäne: gibbhf.local

Systeme & Umgebung
------------------
- vmWS1: Windows Server Manager / Domain Controller
- vmWP1: Windows Client (Domänenmitglied)

AD-Struktur (OUs)
-----------------
- Root-OU: OU=_GibbHF,DC=gibbhf,DC=local
- Clients: OU=Computers,OU=_GibbHF,DC=gibbhf,DC=local (enthält VMWP1)
- Gruppen: OU=Groups,OU=_GibbHF,DC=gibbhf,DC=local
- User-Basis: OU=Users,OU=_GibbHF,DC=gibbhf,DC=local
  - Sub-OU: OU=Lecturers (Dozenten)
  - Sub-OU: OU=Students (Studenten)

Credentials & Konten
--------------------
- Admin: Admin_VMWS1 (Umbenannter lokaler/Domain Admin)
- PW: USE UNIT PWD
- vmWS1 domainadmin PWD: VMADMIN PWD