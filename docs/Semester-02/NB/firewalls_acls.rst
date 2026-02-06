Firewall Matrix & Cisco ACLs
============================

Firewall Rules Matrix
---------------------
Ein Planungstool, um den Kommunikationsfluss zwischen Zonen (z.B. DMZ, Internal, Internet) zu definieren.

* **Definition:** Wer (Source) darf zu wem (Destination) über welchen Dienst (Port/Service) mit welcher Aktion (Permit/Deny)?

Cisco ACL (Access Control Lists)
--------------------------------
Interpretation von Regeln auf Cisco-Systemen:

**Standard ACL (ID 1-99):**
Filtert nur nach der **Quell-IP**.
.. code-block:: cisco

   access-list 10 permit 192.168.10.0 0.0.0.255

**Extended ACL (ID 100-199):**
Filtert nach Quelle, Ziel, Protokoll und Port.
.. code-block:: cisco

   ! Erlaubt TCP von Host A zu Server B auf Port 80 (HTTP)
   access-list 101 permit tcp host 192.168.1.5 host 10.1.1.50 eq 80
   ! Am Ende jeder ACL steht ein "implicit deny any" (alles andere wird geblockt)