==========================================
Webproxy SQUID: Funktionsweise & Nutzen
==========================================

.. raw:: html

   <style>
      .squid-box {
         padding: 15px;
         margin: 15px 0;
         border-radius: 8px;
         color: #333333 !important;
         line-height: 1.5;
         border-left: 8px solid #607d8b; /* Grau-Blau für Proxy */
         background-color: #eceff1;
      }
      
      .squid-title {
         font-weight: bold;
         font-size: 1.25em;
         margin-bottom: 8px;
         color: #000000 !important;
         display: block;
         border-bottom: 1px solid rgba(0,0,0,0.1);
         padding-bottom: 5px;
      }

      .feature-grid {
         display: grid;
         grid-template-columns: 1fr 1fr;
         gap: 10px;
      }

      .feature-item {
         background: white;
         padding: 10px;
         border-radius: 5px;
         border: 1px solid #cfd8dc;
      }

      .exam-tip-squid {
         background-color: #e1f5fe;
         border: 2px dashed #0288d1;
         padding: 15px;
         margin-top: 20px;
         color: #333333 !important;
         border-radius: 5px;
      }
   </style>

Definition: Was ist SQUID?
--------------------------
SQUID ist ein Full-Feature-Webproxy, der auf dem **Application Layer (Layer 7)** arbeitet. Er agiert als "Man-in-the-Middle" zwischen dem internen Client und dem externen Webserver.

.. uml::

   @startuml
   skinparam ParticipantPadding 20
   skinparam BoxPadding 10

   box "Internes Netz" #LightBlue
   participant "Client" as C
   end box

   box "DMZ / Gateway" #LightGrey
   participant "SQUID Proxy" as P
   database "Cache" as D
   end box

   participant "Webserver (Internet)" as W

   == Cache Miss (Erster Aufruf) ==
   C -> P: HTTP Request (www.test.ch)
   P -> D: Check Cache?
   D -> P: Not found (Miss)
   P -> W: Request an Webserver
   W -> P: HTTP Response (Daten)
   P -> D: Speicher Kopie
   P -> C: Daten an Client

   == Cache Hit (Zweiter Aufruf) ==
   C -> P: HTTP Request (www.test.ch)
   P -> D: Check Cache?
   D -> P: Found (Hit)
   P -> C: Daten direkt aus Cache (schnell!)
   @enduml



Die Kernfunktionen im Detail
----------------------------

.. raw:: html

   <div class="squid-box">
      <span class="squid-title">SQUID Hauptaufgaben</span>
      <div class="feature-grid">
         <div class="feature-item">
            <b>1. Caching (Performance)</b><br>
            Speichert Kopien von Webinhalten lokal. 
            <i>Nutzen:</i> Spart Bandbreite (WAN-Entlastung) und reduziert Ladezeiten für User.
         </div>
         <div class="feature-item">
            <b>2. Filterung (Security)</b><br>
            Blockiert URLs, Domains oder Dateitypen (z.B. .exe).
            <i>Nutzen:</i> Schutz vor Malware und Durchsetzung von Firmenrichtlinien.
         </div>
         <div class="feature-item">
            <b>3. Authentifizierung</b><br>
            Identifiziert User (LDAP/AD Integration).
            <i>Nutzen:</i> Nur berechtigte Personen dürfen surfen; personalisierte Regeln möglich.
         </div>
         <div class="feature-item">
            <b>4. Logging (Compliance)</b><br>
            Protokolliert alle Zugriffe (Wer, Wann, Was).
            <i>Nutzen:</i> Rückverfolgbarkeit bei Vorfällen und Reporting der Netzauslastung.
         </div>
      </div>
   </div>

Einsatzgebiete
--------------
* **KMU:** Zentrale Kontrolle des Internetverkehrs.
* **Schulen (Smartlearn):** Jugendschutz durch Inhaltsfilter.
* **Hotellösung:** Bandbreitenmanagement für viele gleichzeitige Nutzer.

.. raw:: html

   <div class="exam-tip-squid">
      <strong>Prüfungs-Fokus:</strong> Erkläre SQUID als "Vermittler". Das wichtigste Stichwort ist <b>Caching</b> zur Bandbreiteneinsparung. SQUID sieht den Inhalt der Pakete (Layer 7), im Gegensatz zu einer reinen Layer-3-Firewall.
   </div>