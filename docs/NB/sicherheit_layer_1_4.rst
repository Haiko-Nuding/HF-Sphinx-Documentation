==========================================
Layer 1 - 4 Netzwerksicherheitsmassnahmen
==========================================

.. raw:: html

   <style>
      /* Grundcontainer für die Layer-Boxen */
      .layer-box {
         padding: 15px;
         margin: 15px 0;
         border-radius: 8px;
         color: #333333 !important; /* Erzwingt dunkle Schriftfarbe */
         line-height: 1.5;
         border-left: 8px solid;
      }

      .layer-title {
         font-weight: bold;
         font-size: 1.25em;
         margin-bottom: 8px;
         color: #000000 !important;
         display: block;
         border-bottom: 1px solid rgba(0,0,0,0.1);
         padding-bottom: 5px;
      }

      /* Spezifische Farben pro Layer für bessere Merkfähigkeit */
      .l1 { background-color: #e8f5e9; border-color: #4caf50; } /* Grün */
      .l2 { background-color: #e3f2fd; border-color: #2196f3; } /* Blau */
      .l3 { background-color: #fff3e0; border-color: #ff9800; } /* Orange */
      .l4 { background-color: #f3e5f5; border-color: #9c27b0; } /* Lila */

      .exam-tip {
         background-color: #fff9c4;
         border: 2px dashed #fbc02d;
         padding: 15px;
         margin-top: 20px;
         color: #333333 !important;
         border-radius: 5px;
      }

      /* Sicherstellen, dass Listenpunkte auch dunkel sind */
      .layer-box ul li {
         color: #333333 !important;
      }
   </style>

Konzept: Defense in Depth
-------------------------
Sicherheit sollte wie eine Zwiebel aufgebaut sein. Versagt eine Schicht, hält die nächste den Angreifer auf.

.. uml::

   @startuml
   skinparam backgroundColor #FFFFFF
   skinparam packageStyle rectangle

   package "Sicherheits-Schichten" {
     rectangle "Layer 4: Transport (TCP/UDP)" as L4 #D1F2EB
     rectangle "Layer 3: Network (IP)" as L3 #A9DFBF
     rectangle "Layer 2: Data Link (MAC)" as L2 #7DCEA0
     rectangle "Layer 1: Physical (Hardware)" as L1 #52BE80

     L4 -down-> L3
     L3 -down-> L2
     L2 -down-> L1
   }
   @enduml

Detaillierte Definitionen (Lernziele)
-------------------------------------

.. raw:: html

   <div class="layer-box l1">
      <span class="layer-title">Layer 1 - Physical Layer</span>
      <ul>
         <li><b>Fokus:</b> Schutz der physischen Infrastruktur und Übertragungsmedien.</li>
         <li><b>Massnahmen:</b> Zutrittskontrolle (Badge), abschliessbare Racks, Verplombung von Netzwerkdosen, Einsatz von physischen Port-Blockern.</li>
      </ul>
   </div>

   <div class="layer-box l2">
      <span class="layer-title">Layer 2 - Data Link Layer</span>
      <ul>
         <li><b>Port-Security:</b> Limitiert MAC-Adressen pro Port; schaltet Port bei unbekannten Geräten ab (Violation).</li>
         <li><b>DHCP Snooping:</b> Filtert DHCP-Pakete; verhindert "Rogue DHCP Server" (falsche IP-Vergabe).</li>
         <li><b>VLANs:</b> Logische Segmentierung zur Reduktion der Broadcast-Domäne und Angriffsfläche.</li>
      </ul>
   </div>

   <div class="layer-box l3">
      <span class="layer-title">Layer 3 - Network Layer</span>
      <ul>
         <li><b>ACLs (Access Control Lists):</b> Paketfilterung nach Source-/Destination-IP (Statisch).</li>
         <li><b>IPsec VPN:</b> Bietet Vertraulichkeit und Integrität für Datenpakete über das Internet.</li>
      </ul>
   </div>

   <div class="layer-box l4">
      <span class="layer-title">Layer 4 - Transport Layer</span>
      <ul>
         <li><b>Stateful Inspection:</b> Firewall prüft, ob Pakete zu einer validen Sitzung gehören (Session-Tracking).</li>
         <li><b>Port-Filterung:</b> Erlaubt/Verbietet Dienste basierend auf TCP/UDP Portnummern (z.B. Port 80, 443).</li>
      </ul>
   </div>

   <div class="exam-tip">
      <strong>Zusammenfassung für die 2 A4-Seiten:</strong><br>
      L1 = Schlösser/Dosen | L2 = MAC/Port-Security/VLAN | L3 = IP/ACL/VPN | L4 = Ports/Stateful Firewall
   </div>