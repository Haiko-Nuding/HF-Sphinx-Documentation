Video Eigene Idee 1
===================

.. important::
   Programm aus 4.1 Eigene Idee 1 für ein Programm


Meine Idee
----------

Als eigene Idee habe ich eine kleine **Self-Destruct-Sequenz** für das ESP32-Board
programmiert. Dabei wollte ich die bereits vorhandenen LEDs, einen Taster und den
Buzzer miteinander kombinieren und nicht nur eine einzelne LED ein- und ausschalten.

Die Sequenz wird mit dem Taster **K1** gestartet. Danach werden mehrere Phasen
nacheinander ausgeführt. Die LEDs stellen dabei verschiedene Zustände der Sequenz
dar. Gegen Ende blinkt die orange LED immer schneller, bevor die rote LED kurz
aufleuchtet und abschliessend ein Sound über den Buzzer abgespielt wird.


Zuordnung der LEDs
------------------

Bevor ich die Sequenz programmierte, musste ich zuerst herausfinden, welche der
vier LEDs auf dem Board zu welcher ``LED``-ID gehört. Die Zuordnung ergibt sich
aus der vorhandenen ``led.yaml`` und wurde anschliessend am Board überprüft.

.. list-table::
   :header-rows: 1
   :widths: 20 25 25

   * - ID
     - Farbe
     - GPIO
   * - ``LED1``
     - Rot
     - ``GPIO25``
   * - ``LED2``
     - Grün
     - ``GPIO14``
   * - ``LED3``
     - Blau
     - ``GPIO13``
   * - ``LED4``
     - Orange
     - ``GPIO12``


Ablauf der Self-Destruct-Sequenz
--------------------------------

Die Sequenz läuft nach dem Drücken von **K1** automatisch ab:

#. Zu Beginn werden alle vier LEDs ausgeschaltet, damit ein definierter
   Ausgangszustand vorhanden ist.
#. Die grüne LED leuchtet kurz auf.
#. Anschliessend blinken die grüne und die blaue LED gemeinsam für ungefähr
   drei Sekunden.
#. Grün und Blau werden ausgeschaltet.
#. Die orange LED beginnt zu blinken.
#. Die Abstände des Blinkens werden schrittweise kleiner, wodurch ein
   beschleunigter Countdown entsteht.
#. Nach dem schnellen Blinken wird die orange LED ausgeschaltet.
#. Nach einer kurzen Pause leuchtet die rote LED für eine Sekunde.
#. Die rote LED wird wieder ausgeschaltet.
#. Als Abschluss wird über den Buzzer eine kurze abfallende Tonfolge als
   Boom-/Shutdown-Effekt abgespielt.
#. Danach bleiben alle LEDs ausgeschaltet.


Programmierung der Sequenz
--------------------------

Die eigentliche Logik habe ich in einer eigenen YAML-Datei für die
Self-Destruct-Sequenz umgesetzt. Dadurch bleibt die ``main.yaml`` übersichtlich
und die eigene Funktion ist vom restlichen Demo-Projekt getrennt.


``self_destruct.yaml``
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Eigene Self-Destruct-Sequenz
   #
   # LED1 = Rot
   # LED2 = Grün
   # LED3 = Blau
   # LED4 = Orange
   #
   # Ablauf:
   # 1. Grün leuchtet kurz
   # 2. Grün und Blau blinken gemeinsam für ca. 3 Sekunden
   # 3. Grün und Blau gehen aus
   # 4. Orange blinkt ca. 5 Sekunden immer schneller
   # 5. Orange geht aus
   # 6. Rot leuchtet 1 Sekunde
   # 7. Rot geht aus
   # 8. Boom-Sound
   # 9. Alle LEDs bleiben aus

   script:
     - id: self_destruct_sequence
       mode: restart
       then:

         # STARTZUSTAND

         # Alle LEDs zuerst ausschalten
         - switch.turn_off: LED1
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - switch.turn_off: LED4
         - delay: 250ms


         # PHASE 1: SYSTEM WIRD AKTIVIERT

         # Zuerst leuchtet nur Grün
         - switch.turn_on: LED2
         - delay: 500ms
         - switch.turn_off: LED2
         - delay: 200ms


         # PHASE 2: GRÜN + BLAU BLINKEN
         # Beide LEDs blinken gemeinsam für ca. 3 Sekunden

         # 1
         - switch.turn_on: LED2
         - switch.turn_on: LED3
         - delay: 300ms
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - delay: 300ms

         # 2
         - switch.turn_on: LED2
         - switch.turn_on: LED3
         - delay: 300ms
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - delay: 300ms

         # 3
         - switch.turn_on: LED2
         - switch.turn_on: LED3
         - delay: 300ms
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - delay: 300ms

         # 4
         - switch.turn_on: LED2
         - switch.turn_on: LED3
         - delay: 300ms
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - delay: 300ms

         # 5
         - switch.turn_on: LED2
         - switch.turn_on: LED3
         - delay: 300ms
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - delay: 300ms


         # PHASE 3: COUNTDOWN
         # Orange blinkt immer schneller

         - switch.turn_on: LED4
         - delay: 500ms
         - switch.turn_off: LED4
         - delay: 500ms

         - switch.turn_on: LED4
         - delay: 400ms
         - switch.turn_off: LED4
         - delay: 400ms

         - switch.turn_on: LED4
         - delay: 300ms
         - switch.turn_off: LED4
         - delay: 300ms

         - switch.turn_on: LED4
         - delay: 250ms
         - switch.turn_off: LED4
         - delay: 250ms

         - switch.turn_on: LED4
         - delay: 200ms
         - switch.turn_off: LED4
         - delay: 200ms


         # COUNTDOWN BESCHLEUNIGT

         - switch.turn_on: LED4
         - delay: 150ms
         - switch.turn_off: LED4
         - delay: 150ms

         - switch.turn_on: LED4
         - delay: 120ms
         - switch.turn_off: LED4
         - delay: 120ms

         - switch.turn_on: LED4
         - delay: 100ms
         - switch.turn_off: LED4
         - delay: 100ms

         - switch.turn_on: LED4
         - delay: 80ms
         - switch.turn_off: LED4
         - delay: 80ms

         - switch.turn_on: LED4
         - delay: 60ms
         - switch.turn_off: LED4
         - delay: 60ms


         # PHASE 4: KRITISCH
         # Orange blinkt extrem schnell

         - switch.turn_on: LED4
         - delay: 50ms
         - switch.turn_off: LED4
         - delay: 50ms

         - switch.turn_on: LED4
         - delay: 40ms
         - switch.turn_off: LED4
         - delay: 40ms

         - switch.turn_on: LED4
         - delay: 30ms
         - switch.turn_off: LED4
         - delay: 30ms

         - switch.turn_on: LED4
         - delay: 25ms
         - switch.turn_off: LED4
         - delay: 25ms

         - switch.turn_on: LED4
         - delay: 20ms
         - switch.turn_off: LED4
         - delay: 20ms

         - switch.turn_on: LED4
         - delay: 15ms
         - switch.turn_off: LED4
         - delay: 15ms

         # Orange sicher ausschalten
         - switch.turn_off: LED4


         # PHASE 5: ABRUPTER STOP

         # Nach dem schnellen Blinken kurz komplette Dunkelheit
         - delay: 300ms


         # PHASE 6: LETZTE WARNUNG

         # Rot leuchtet für genau 1 Sekunde
         - switch.turn_on: LED1
         - delay: 1s
         - switch.turn_off: LED1

         # Kurze Pause vor dem Boom
         - delay: 300ms


         # PHASE 7: BOOM

         # Abfallende Tonfolge als Boom-/Shutdown-Effekt
         - rtttl.play: 'self_destruct:d=16,o=5,b=240:8c6,8g5,8e5,8c5,16g4,16e4,4c4'

         # Sound fertig spielen lassen
         - delay: 1500ms


         # ENDZUSTAND

         # Nach der Self-Destruct-Sequenz bleiben alle LEDs aus
         - switch.turn_off: LED1
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - switch.turn_off: LED4


Start über den Taster
---------------------

Damit die Sequenz gestartet werden kann, habe ich den bereits vorhandenen
Taster **K1** angepasst. Beim Drücken wird nicht mehr nur eine einzelne LED
geschaltet, sondern das Script ``self_destruct_sequence`` ausgeführt.

Der zweite Taster **K2** bleibt unabhängig davon bestehen und spielt weiterhin
die bereits vorhandene Tonfolge ab.


``button.yaml``
~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Konfiguration der beiden Taster auf dem Board

   binary_sensor:

     # K1 startet meine eigene Self-Destruct-Sequenz
     - platform: gpio
       id: "ButtonK1"
       name: "Button K1"
       device_class: door
       pin:
         number: GPIO23
         mode: INPUT_PULLUP
         inverted: true
       on_press:
         then:
           - script.execute: self_destruct_sequence

     # K2 spielt weiterhin die vorhandene Tonfolge ab
     - platform: gpio
       id: "ButtonK2"
       name: "Button K2"
       pin:
         number: GPIO19
         mode: INPUT_PULLUP
         inverted: true
       on_press:
         then:
           - rtttl.play: 'scale_up:d=32,o=5,b=100:c,c#,d#,e,f#,g#,a#,b'


Überprüfung der YAML-Konfiguration
----------------------------------

Bevor ich das Programm auf den ESP32 übertragen habe, habe ich zuerst die
gesamte ESPHome-Konfiguration überprüft:

.. code-block:: powershell

   esphome config .\main.yaml

Damit konnte ich überprüfen, ob die YAML-Struktur und die eingebundenen
Komponenten von ESPHome korrekt erkannt werden.


Übertragung auf den ESP32
-------------------------

Nach der erfolgreichen Prüfung habe ich die neue Konfiguration kompiliert und
auf den ESP32 übertragen:

.. code-block:: powershell

   esphome run .\main.yaml

Da der ESP32 bereits mit meinem iPhone-Hotspot verbunden und eingerichtet war,
konnte ich die neue Version **OTA (Over the Air)** übertragen. Dadurch musste
ich das Board für die Änderungen nicht erneut über USB flashen.

Während des Tests konnte ich zusätzlich die Live-Logs von ESPHome direkt im
Terminal verfolgen.


Ergebnis
--------

Beim Drücken von **K1** wird die komplette Self-Destruct-Sequenz ausgeführt.
Zuerst werden Grün und Blau verwendet. Danach blinkt die orange LED mit immer
kürzeren Abständen und wird dadurch sichtbar schneller. Zum Schluss leuchtet
die rote LED für eine Sekunde auf und der Buzzer spielt die definierte Tonfolge
ab.

Nach Abschluss der Sequenz bleiben alle LEDs ausgeschaltet.


Videonachweis
-------------

.. youtube:: U51Ra8-ciNs
   :width: 100%


Was ich dabei gelernt habe
--------------------------

Bei der Umsetzung habe ich besser verstanden, wie ich mit ESPHome mehrere LEDs
und den Buzzer zu einem eigenen Ablauf kombinieren kann. Besonders hilfreich
fand ich die **Live-Logs**. Beim ersten Test hatte ich ein Problem mit dem Sound
und konnte in den Logs direkt erkennen, dass der Fehler bei der RTTTL-Tonfolge
lag.

Praktisch fand ich auch, dass ich meine Änderungen zuerst mit ``esphome config``
prüfen und danach direkt **OTA** auf den ESP32 übertragen konnte. Dadurch konnte
ich die Sequenz schnell anpassen und erneut ausprobieren.