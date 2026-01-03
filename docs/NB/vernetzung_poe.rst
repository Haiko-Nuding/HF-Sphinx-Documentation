==========================================
Standortvernetzung & PoE
==========================================

.. raw:: html

   <style>
      .poe-vpn-content {
         line-height: 1.6;
      }

      .custom-card {
         padding: 15px;
         margin: 15px 0;
         border-radius: 8px;
         border-left: 8px solid;
      }

      /* Farben für Standortvernetzung (Blau) */
      .vpn-card {
         background-color: #e3f2fd;
         border-color: #1976d2;
      }

      /* Farben für PoE (Grün) */
      .poe-card {
         background-color: #f1f8e9;
         border-color: #43a047;
      }

      /* Schriftfarben-Fix */
      .custom-card, .custom-card *, .poe-table, .poe-table * {
         color: #212121 !important;
      }

      .card-title {
         font-weight: bold;
         font-size: 1.2em;
         display: block;
         margin-bottom: 10px;
         text-transform: uppercase;
      }

      .poe-table {
         width: 100%;
         border-collapse: collapse;
         background-color: rgba(255, 255, 255, 0.5);
         margin-top: 10px;
      }

      .poe-table th, .poe-table td {
         border: 1px solid #ccc;
         padding: 8px;
         text-align: left;
      }

      .poe-table th {
         background-color: rgba(0, 0, 0, 0.05);
      }
   </style>

.. raw:: html

   <div class="poe-vpn-content">

Standortvernetzung (WAN-Technologien)
-------------------------------------
Wahl der Verbindung basierend auf der Ausgangslage (Kosten vs. Qualität).

.. uml::

   @startuml
   skinparam packageStyle rectangle
   
   node "Zentrale" as HQ #LawnGreen
   node "Filiale" as Branch #SkyBlue
   
   cloud "Internet" as Cloud1
   cloud "Provider Netz (MPLS)" as Cloud2
   
   HQ <..> Cloud1 : IPsec VPN (Günstig)
   Cloud1 <..> Branch
   
   HQ <-> Cloud2 : MPLS (Garantierte QoS)
   Cloud2 <-> Branch
   @enduml



.. raw:: html

      <div class="custom-card vpn-card">
         <span class="card-title">VPN & MPLS im Vergleich</span>
         <ul>
            <li><b>IPsec VPN:</b> Bietet einen verschlüsselten Tunnel über das öffentliche Internet. 
                <i>Vorteil:</i> Kostengünstig und überall verfügbar. <i>Nachteil:</i> Keine Bandbreitengarantie.</li>
            <li><b>MPLS:</b> Eine dedizierte Leitung vom Provider. 
                <i>Vorteil:</i> Garantierte Performance und Quality of Service (QoS). <i>Nachteil:</i> Sehr teuer.</li>
            <li><b>Site-to-Site:</b> Die feste Kopplung von zwei Standorten (Router-zu-Router).</li>
         </ul>
      </div>

Power over Ethernet (PoE)
-------------------------
Zentrale Stromversorgung von Netzwerkgeräten über das Ethernet-Kabel.



.. raw:: html

      <div class="custom-card poe-card">
         <span class="card-title">Beschaffungskriterien & Standards</span>
         <p>Beim Kauf von Switches müssen zwei Faktoren zwingend geprüft werden:</p>
         <ol>
            <li><b>PoE Budget:</b> Die totale Wattleistung, die der Switch liefern kann (muss > Summe aller Endgeräte sein).</li>
            <li><b>PoE Standard:</b> Bestimmt die maximale Leistung pro Port.</li>
         </ol>

         <table class="poe-table">
            <thead>
               <tr>
                  <th>Standard</th>
                  <th>Bezeichnung</th>
                  <th>Leistung</th>
                  <th>Einsatzbeispiel</th>
               </tr>
            </thead>
            <tbody>
               <tr>
                  <td><b>802.3af</b></td>
                  <td>PoE</td>
                  <td>bis 15.4W</td>
                  <td>IP-Telefone, Sensoren</td>
               </tr>
               <tr>
                  <td><b>802.3at</b></td>
                  <td>PoE+</td>
                  <td>bis 30W</td>
                  <td>WLAN WiFi-6 APs, Kameras</td>
               </tr>
               <tr>
                  <td><b>802.3bt</b></td>
                  <td>PoE++</td>
                  <td>bis 60W / 90W</td>
                  <td>Smart Displays, Laptops</td>
               </tr>
            </tbody>
         </table>
      </div>

   </div>