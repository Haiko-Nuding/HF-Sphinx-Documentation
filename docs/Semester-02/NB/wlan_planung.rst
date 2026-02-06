==========================================
WLAN Realisierung & Survey
==========================================

.. raw:: html

   <style>
      /* Nur CSS für spezifische Klassen, um Kollisionen zu vermeiden */
      .wlan-content-all {
         line-height: 1.6;
      }

      .phase-box {
         padding: 15px;
         margin: 10px 0;
         border-radius: 8px;
         border-left: 8px solid;
         background-color: #ffffff;
         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }

      /* Schriftfarben innerhalb der Boxen auf Dunkel zwingen */
      .phase-box, .phase-box *, .metric-box, .metric-box *, .exam-hint-wlan, .exam-hint-wlan * {
         color: #333333 !important;
      }

      .p1 { border-color: #9e9e9e; background-color: #f5f5f5; }
      .p2 { border-color: #2196f3; background-color: #e3f2fd; }
      .p3 { border-color: #4caf50; background-color: #e8f5e9; }

      .phase-title {
         font-weight: bold;
         font-size: 1.1em;
         display: block;
         margin-bottom: 5px;
         text-transform: uppercase;
      }

      .metric-container {
         display: flex;
         gap: 15px;
         margin: 20px 0;
      }

      .metric-box {
         background-color: #fff3e0;
         border: 2px solid #ffb74d;
         padding: 15px;
         flex: 1;
         border-radius: 8px;
      }

      .metric-box b { color: #e65100 !important; }

      .exam-hint-wlan {
         background-color: #ffebee;
         border: 2px solid #ef5350;
         padding: 15px;
         margin-top: 20px;
         border-radius: 8px;
      }
      .exam-hint-wlan strong { color: #c62828 !important; }
   </style>

.. raw:: html

   <div class="wlan-content-all">

Der Workflow einer WLAN-Realisierung
------------------------------------
Eine professionelle WLAN-Planung folgt einem festen Zyklus.

.. uml::

   @startuml
   skinparam activityFontSize 12
   start
   :Anforderungsaufnahme;
   #silver:Predictive Survey\n(Simulation);
   #lightblue:On-Site Survey\n(Messung vor Ort);
   #lightgreen:Installation;
   #lightgreen:Post-Deployment Survey\n(Validierung);
   stop
   @enduml



Die Phasen im Detail
--------------------

.. raw:: html

      <div class="phase-box p1">
         <span class="phase-title">1. Vorbereitung & Simulation</span>
         <ul>
            <li><b>Anforderungsaufnahme:</b> Klärung von Useranzahl und Applikationen (z.B. Echtzeit-Voice).</li>
            <li><b>Predictive Survey:</b> Rein softwarebasiert. Einzeichnen von Wänden in Baupläne. Ziel: Grobe AP-Anzahl bestimmen.</li>
         </ul>
      </div>

      <div class="phase-box p2">
         <span class="phase-title">2. Messung & Verifikation</span>
         <ul>
            <li><b>On-Site Survey (AP-on-a-Stick):</b> Physische Messung vor Ort. Findet reale Störquellen (Mikrowellen, DFS) und prüft Wanddämpfung.</li>
         </ul>
      </div>

      <div class="phase-box p3">
         <span class="phase-title">3. Umsetzung & Abschluss</span>
         <ul>
            <li><b>Installation:</b> Montage der Hardware.</li>
            <li><b>Post-Deployment Survey:</b> Abschlussmessung. Beweist, dass die Ziele erreicht wurden.</li>
         </ul>
      </div>

Wichtige physikalische Faktoren
-------------------------------



.. raw:: html

      <div class="metric-container">
         <div class="metric-box">
            <b>RSSI (Signalstärke)</b><br>
            Gemessen in dBm. Je näher an 0 (z.B. -30), desto stärker das Signal.<br>
            <i>Prüfungswert:</i> Mindestens <b>-67 dBm</b> für Voice.
         </div>
         <div class="metric-box">
            <b>SNR (Signal-to-Noise Ratio)</b><br>
            Abstand zwischen Nutzsignal und Rauschen.<br>
            <i>Ziel:</i> Ein hoher SNR sorgt für weniger Fehler und mehr Speed.
         </div>
      </div>

.. raw:: html

      <div class="exam-hint-wlan">
         <strong>Prüfungs-Falle:</strong> Ein Predictive Survey ersetzt <u>nie</u> den On-Site Survey. Nur vor Ort können Interferenzen zuverlässig erkannt werden. Der Wert <b>-67 dBm</b> ist die kritische Grenze für Business-WLAN.
      </div>

   </div>