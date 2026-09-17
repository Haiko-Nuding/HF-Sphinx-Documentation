Video LED ein und ausschalten
=============================

.. important::
    Programm aus 4.1 zum ein und ausschalten der LED mit Video belegt.


LED mit Taster steuern
----------------------

Für diese Aufgabe habe ich die bereits vorhandene Konfiguration des Demo-Projekts
verwendet. Der Taster **K1** ist mit ``GPIO23`` verbunden. Beim Drücken des
Tasters wird die **gelbe LED (LED4)** eingeschaltet, bleibt für **1,5 Sekunden**
an und wird anschliessend automatisch wieder ausgeschaltet.

Die dafür relevante Konfiguration befindet sich in der Datei ``button.yaml``.


Programm
--------

.. code-block:: yaml

   binary_sensor:
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
           - switch.turn_on: LED4
           - delay: 1500ms
           - switch.turn_off: LED4


Funktionsweise
--------------

Beim Drücken von **K1** wird das Ereignis ``on_press`` ausgelöst. ESPHome führt
daraufhin die drei definierten Schritte nacheinander aus:

#. Gelbe LED (``LED4``) einschalten
#. 1,5 Sekunden warten
#. Gelbe LED (``LED4``) wieder ausschalten

Ich habe die Funktion direkt am ESP32 getestet und anschliessend in einem kurzen
Video festgehalten.


Videonachweis
-------------

.. youtube:: OTkN6PLQ4nQ
   :width: 100%