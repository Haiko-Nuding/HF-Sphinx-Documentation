Video Eigene Idee 2
===================

.. important::
   Programm aus 4.1 Eigene Idee 2 für ein Programm


Meine Idee
----------

Als zweite eigene Idee habe ich eine **WiFi-Qualitätsanzeige** für das ESP32-Board
programmiert.

Mein ESP32 ist während der Arbeit mit meinem mobilen Hotspot verbunden. Dadurch
kann ich die aktuelle WLAN-Signalstärke messen und mit den vier vorhandenen LEDs
direkt auf dem Board anzeigen.

Die vier LEDs funktionieren dabei ähnlich wie die Balkenanzeige für den
Mobilfunk- oder WLAN-Empfang bei einem Smartphone.

Je besser die Verbindung zum Hotspot ist, desto mehr LEDs leuchten.

Damit verbinde ich in dieser Aufgabe:

* den WiFi-Signal-Sensor von ESPHome,
* die WLAN-Verbindung meines ESP32,
* vier vorhandene LEDs,
* eine Umrechnung von dBm in Prozent,
* Bedingungen für verschiedene Signalstärken.


Idee der Balkenanzeige
----------------------

Die Signalstärke wird als Prozentwert zwischen ``0 %`` und ``100 %`` dargestellt.

Abhängig von diesem Wert werden unterschiedlich viele LEDs eingeschaltet.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - WiFi-Signal
     - Anzahl LEDs
     - Anzeige
   * - 1 % bis unter 25 %
     - 1 LED
     - Sehr schwach
   * - 25 % bis unter 50 %
     - 2 LEDs
     - Schwach
   * - 50 % bis unter 75 %
     - 3 LEDs
     - Gut
   * - 75 % bis 100 %
     - 4 LEDs
     - Sehr gut

Wenn keine Verbindung zum Hotspot vorhanden ist, wird nur die rote LED
eingeschaltet. Dadurch ist sofort sichtbar, dass der ESP32 nicht mit dem WLAN
verbunden ist.


Verwendete LEDs
---------------

Für die Anzeige verwende ich die bereits vorhandenen vier LEDs des Boards.

.. list-table::
   :header-rows: 1
   :widths: 25 30 30

   * - LED-ID
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

Für diese Aufgabe verwende ich die LEDs nicht hauptsächlich nach ihrer Farbe,
sondern als Balken.

Die Reihenfolge der Balkenanzeige ist:

.. code-block:: text

   1 LED:

   LED1  ON
   LED2  OFF
   LED3  OFF
   LED4  OFF


   2 LEDs:

   LED1  ON
   LED2  ON
   LED3  OFF
   LED4  OFF


   3 LEDs:

   LED1  ON
   LED2  ON
   LED3  ON
   LED4  OFF


   4 LEDs:

   LED1  ON
   LED2  ON
   LED3  ON
   LED4  ON


WiFi-Signal messen
------------------

ESPHome besitzt einen eigenen ``wifi_signal``-Sensor.

Dieser Sensor liefert die WLAN-Signalstärke normalerweise in ``dBm``.

Ein Wert nahe bei ``-50 dBm`` bedeutet eine gute Verbindung. Je stärker der
Wert in den negativen Bereich fällt, desto schlechter wird normalerweise die
Verbindung.

Für meine Anzeige möchte ich jedoch einen einfacher verständlichen Prozentwert
verwenden.

Deshalb erstelle ich zuerst einen Sensor für den ursprünglichen dBm-Wert und
danach einen zweiten Sensor, welcher diesen Wert ungefähr in einen Bereich von
``0 %`` bis ``100 %`` umrechnet.


``wifi_signal.yaml``
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   sensor:

     # Ursprüngliche WLAN-Signalstärke in dBm
     - platform: wifi_signal
       id: wifi_signal_db
       name: "WiFi Signal dBm"
       update_interval: 2s


     # Umrechnung der Signalstärke in Prozent
     - platform: copy
       source_id: wifi_signal_db
       id: wifi_signal_percent
       name: "WiFi Signal Percent"
       unit_of_measurement: "%"
       icon: "mdi:wifi"

       filters:
         - lambda: |-
             float percent = 2.0 * (x + 100.0);

             if (percent > 100.0) {
               percent = 100.0;
             }

             if (percent < 0.0) {
               percent = 0.0;
             }

             return percent;


Umrechnung von dBm in Prozent
-----------------------------

Für die Balkenanzeige verwende ich eine einfache Umrechnung.

Die verwendete Formel lautet:

.. code-block:: text

   Prozent = 2 × (dBm + 100)

Danach wird der Wert auf einen Bereich zwischen ``0`` und ``100`` begrenzt.

Einige Beispiele:

.. list-table::
   :header-rows: 1
   :widths: 30 30

   * - Signalstärke
     - ungefährer Prozentwert
   * - ``-50 dBm``
     - ``100 %``
   * - ``-60 dBm``
     - ``80 %``
   * - ``-70 dBm``
     - ``60 %``
   * - ``-80 dBm``
     - ``40 %``
   * - ``-90 dBm``
     - ``20 %``

Der Prozentwert dient bei diesem Projekt hauptsächlich dazu, die Signalstärke
einfach auf vier Bereiche aufzuteilen.

Es handelt sich deshalb nicht um eine exakte physikalische Prozentmessung,
sondern um eine gut verständliche Darstellung der WLAN-Signalqualität.


WiFi-Verbindungsstatus
----------------------

Zusätzlich zur Signalstärke möchte ich erkennen können, ob der ESP32 überhaupt
mit meinem Hotspot verbunden ist.

Dafür verwende ich einen internen ESPHome-Statussensor.

Dieser Sensor muss nicht zusätzlich im Webinterface angezeigt werden. Er wird
nur innerhalb der WiFi-LED-Steuerung verwendet.


WiFi-Qualitätsanzeige programmieren
-----------------------------------

Die eigentliche Steuerung speichere ich in einer eigenen Datei
``wifi_quality.yaml``.

Dadurch bleibt die ``main.yaml`` übersichtlich und die Logik meiner zweiten
eigenen Idee befindet sich in einer eigenen Datei.

Die LED-Anzeige wird alle zwei Sekunden aktualisiert.

Zuerst werden alle LEDs ausgeschaltet.

Anschliessend wird geprüft, ob der ESP32 noch mit dem WLAN verbunden ist.

Wenn keine Verbindung vorhanden ist, wird nur ``LED1`` eingeschaltet.

Wenn eine Verbindung vorhanden ist, wird der aktuelle Prozentwert ausgewertet
und die entsprechende Anzahl LEDs eingeschaltet.


``wifi_quality.yaml``
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Eigene Idee 2
   # WiFi-Qualitaetsanzeige mit vier LEDs
   #
   # LED1 = Rot
   # LED2 = Gruen
   # LED3 = Blau
   # LED4 = Orange
   #
   # 1 - 24 %   -> 1 LED
   # 25 - 49 %  -> 2 LEDs
   # 50 - 74 %  -> 3 LEDs
   # 75 - 100 % -> 4 LEDs
   #
   # Keine WLAN-Verbindung:
   # Nur LED1 leuchtet


   binary_sensor:

     # Interner Status der ESPHome-Verbindung
     - platform: status
       id: wifi_connection_status
       internal: true


   interval:

     - interval: 2s
       then:

         # Zuerst alle LEDs ausschalten
         - switch.turn_off: LED1
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - switch.turn_off: LED4


         # Prüfen, ob der ESP32 verbunden ist
         - if:
             condition:
               binary_sensor.is_off: wifi_connection_status

             then:

               # Keine Verbindung -> rote LED
               - switch.turn_on: LED1

             else:

               # Verbindung vorhanden
               # Balkenanzeige abhängig von der Signalqualität


               # Ab 1 % -> LED1
               - if:
                   condition:
                     lambda: |-
                       return !isnan(id(wifi_signal_percent).state) &&
                              id(wifi_signal_percent).state >= 1.0;
                   then:
                     - switch.turn_on: LED1


               # Ab 25 % -> LED2 zusätzlich
               - if:
                   condition:
                     lambda: |-
                       return !isnan(id(wifi_signal_percent).state) &&
                              id(wifi_signal_percent).state >= 25.0;
                   then:
                     - switch.turn_on: LED2


               # Ab 50 % -> LED3 zusätzlich
               - if:
                   condition:
                     lambda: |-
                       return !isnan(id(wifi_signal_percent).state) &&
                              id(wifi_signal_percent).state >= 50.0;
                   then:
                     - switch.turn_on: LED3


               # Ab 75 % -> LED4 zusätzlich
               - if:
                   condition:
                     lambda: |-
                       return !isnan(id(wifi_signal_percent).state) &&
                              id(wifi_signal_percent).state >= 75.0;
                   then:
                     - switch.turn_on: LED4


Warum mehrere LEDs gleichzeitig leuchten
----------------------------------------

Bei dieser Aufgabe verwende ich bewusst eine Balkenanzeige.

Deshalb werden die LEDs nicht einzeln für bestimmte Bereiche verwendet.

Bei einer guten Verbindung bleiben auch die LEDs der niedrigeren Stufen
eingeschaltet.

Beispielsweise bedeutet ein Signalwert von ``80 %``:

.. code-block:: text

   Signal: 80 %

   LED1: ON
   LED2: ON
   LED3: ON
   LED4: ON

Bei einem Wert von ``55 %`` sieht die Anzeige dagegen so aus:

.. code-block:: text

   Signal: 55 %

   LED1: ON
   LED2: ON
   LED3: ON
   LED4: OFF

Bei einem schwachen Signal von ``30 %``:

.. code-block:: text

   Signal: 30 %

   LED1: ON
   LED2: ON
   LED3: OFF
   LED4: OFF

Dadurch lässt sich die Signalqualität bereits aus einiger Entfernung am Board
erkennen.


Vorhandene LED-Konfiguration
----------------------------

Die Definition der vier LEDs befindet sich weiterhin in meiner bestehenden
``led.yaml``.

Für diese Aufgabe muss die Pinbelegung nicht verändert werden.


``led.yaml``
~~~~~~~~~~~~

.. code-block:: yaml

   # Hier werden die LED's angesteuert

   switch:

     - platform: gpio
       id: "LED1"
       name: "LED1"
       icon: "mdi:led-on"
       pin: GPIO25


     - platform: gpio
       id: "LED2"
       name: "LED2"
       icon: "mdi:led-on"
       pin: GPIO14


     - platform: gpio
       id: "LED3"
       name: "LED3"
       icon: "mdi:led-on"
       pin: GPIO13


     - platform: gpio
       id: "LED4"
       name: "LED4"
       icon: "mdi:led-on"
       pin: GPIO12


     - platform: restart
       name: "Restart"


Konflikt mit der Temperatur-LED-Steuerung
-----------------------------------------

In einer vorherigen Aufgabe habe ich bereits eine automatische LED-Steuerung
abhängig von der Temperatur erstellt.

Diese befindet sich in:

.. code-block:: text

   temperature_led.yaml

Diese Steuerung überprüft ebenfalls regelmässig einen Sensorwert und verändert
dieselben vier LEDs.

Wenn ``temperature_led.yaml`` und ``wifi_quality.yaml`` gleichzeitig aktiv
wären, würden deshalb zwei unterschiedliche Programme versuchen, dieselben
LEDs zu steuern.

Beispielsweise könnte die WiFi-Steuerung vier LEDs einschalten und bereits eine
Sekunde später könnte die Temperatursteuerung wieder drei davon ausschalten.

Deshalb deaktiviere ich für den Test meiner zweiten eigenen Idee die
Temperatur-LED-Steuerung in der ``main.yaml``.


Anpassung der ``main.yaml``
---------------------------

In der ``main.yaml`` füge ich die neue Datei ``wifi_quality.yaml`` hinzu.

Die bereits vorhandene ``wifi_signal.yaml`` wird weiterhin eingebunden.

Die bisherige Datei ``temperature_led.yaml`` wird für diesen Versuch
auskommentiert, damit nur meine WiFi-Anzeige die vier LEDs steuert.

Die restliche Grundkonfiguration des ESP32 bleibt bestehen.


``main.yaml``
~~~~~~~~~~~~~

.. code-block:: yaml

   substitutions:
     name: haiko #My not be longer then 10 letters
     ssid: !secret ssid
     ssid_pass: !secret ssid_pass
     webserver_user: !secret webserver_user
     webserver_pass: !secret webserver_pass
     fallback_pass: !secret fallback_pass

     #static_ip: 10.130.1.21
     #gateway: 10.130.1.1
     #subnet: 255.255.255.0


   # Basic configuration for an ESP32 device
   esphome:
     name: ${name}
     friendly_name: ${name}


   # Hardware configuration
   esp32:
     board: esp32dev
     framework:
       type: arduino


   # Enable Home Assistant API
   api:


   # Enable over-the-air updates
   ota:
     - platform: esphome


   wifi:
     ssid: ${ssid}
     password: ${ssid_pass}

     ap:
       ssid: ESPHome ${name}
       password: ${fallback_pass}


   captive_portal:


   # Enable logging
   logger:
     level: DEBUG
     #level: VERBOSE


   web_server:
     port: 80
     auth:
       username: ${webserver_user}
       password: ${webserver_pass}


   time:
     - platform: sntp
       id: sntp_time
       timezone: Europe/Zurich
       servers:
         - 0.pool.ntp.org
         - 1.pool.ntp.org
         - 2.pool.ntp.org


   # I2C Config
   i2c:

     # ESP8266
     #sda: 4
     #scl: 5

     # ESP32
     sda: 21
     scl: 22
     scan: True
     id: bus_a


   packages:

     # Include the remote receiver configuration
     #ir: !include ir_remote_receiver.yaml


     # Include the DHT sensor configuration
     dht: !include dht.yaml


     # Include the BMP280 sensor configuration
     #bmp280: !include bmp280.yaml


     # Include the ADC sensor configuration
     adc: !include adc.yaml


     # Include the TM1637 display configuration
     tm1637: !include tm1637.yaml


     # Include the WiFi signal sensor configuration
     wifi_signal: !include wifi_signal.yaml


     # Include the buzzer configuration
     rtttl: !include buzzer.yaml


     # Include the button configuration
     button: !include button.yaml


     # Include the LED configuration
     led: !include led.yaml


     # Include the select configuration
     select: !include select.yaml


     # Include the startup configuration
     startup: !include startup.yaml


     # Include my custom Self-Destruct LED sequence
     self_destruct: !include self_destruct.yaml


     # Temperatursteuerung verwendet ebenfalls die LEDs.
     # Deshalb ist sie während der WiFi-Anzeige deaktiviert.
     #temperature_led: !include temperature_led.yaml


     # Eigene Idee 2:
     # WiFi-Signalqualität mit vier LEDs anzeigen
     wifi_quality: !include wifi_quality.yaml


     # LCD is not used with my current hardware setup
     #lcd: !include lcd_pcf8574.yaml


     # Include the FastLED configuration
     #fastled: !include fastled.yaml


Änderung an der bisherigen WiFi-Steuerung
-----------------------------------------

In meiner bisherigen ``main.yaml`` wurden ``LED1`` und ``LED2`` direkt über
``on_connect`` und ``on_disconnect`` verändert.

Für die neue WiFi-Balkenanzeige verwende ich diese Aktionen nicht mehr.

Der Grund dafür ist derselbe wie bei der Temperatursteuerung: Die LEDs sollen
während dieser Aufgabe nur von ``wifi_quality.yaml`` gesteuert werden.

Die Verbindung selbst bleibt selbstverständlich unverändert.

Der ESP32 verbindet sich weiterhin mit dem in ``secrets.yaml`` definierten
Hotspot:

.. code-block:: yaml

   wifi:
     ssid: ${ssid}
     password: ${ssid_pass}


Aufbau des Programms
--------------------

Die Signalverarbeitung lässt sich vereinfacht folgendermassen darstellen:

.. code-block:: text

                Smartphone-Hotspot
                        |
                        |
                        v
               WLAN-Verbindung
                        |
                        v
               ESP32 WiFi-Sensor
                        |
                        v
                Signal in dBm
                        |
                        v
             Umrechnung in Prozent
                        |
                        v
              wifi_signal_percent
                        |
                        v
              +----------------+
              | LED-Steuerung  |
              +----------------+
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        LED1          LED2          LED3          LED4


Beispiel mit meinem Hotspot
---------------------------

Mein ESP32 verbindet sich für diese Aufgabe mit meinem mobilen Hotspot.

Im ESPHome-Webinterface kann ich neben dem Namen des verbundenen WLANs auch
die aktuelle Signalstärke sehen.

Wenn sich das Smartphone nahe beim ESP32 befindet, sollte die Verbindung
normalerweise stärker sein und entsprechend sollten mehrere LEDs leuchten.

Wenn ich mich mit dem Smartphone vom Board entferne oder das Signal durch
Hindernisse abschwäche, sollte der Prozentwert sinken.

Dadurch sollten schrittweise weniger LEDs leuchten.

Genau dieses Verhalten kann ich später im Video demonstrieren.


Funktionstest
-------------

Nach dem Übertragen der Konfiguration teste ich die WiFi-Anzeige mit meinem
Hotspot.

Dazu kann ich den Abstand zwischen Smartphone und ESP32 verändern.

Der Test besteht aus mehreren Schritten:

#. ESP32 und Smartphone befinden sich zunächst nahe beieinander.
#. Ich überprüfe den aktuellen Wert von ``WiFi Signal Percent``.
#. Ich kontrolliere, wie viele LEDs eingeschaltet sind.
#. Anschliessend entferne ich mich mit dem Smartphone vom ESP32.
#. Ich beobachte, ob die Signalstärke sinkt.
#. Ich kontrolliere, ob entsprechend weniger LEDs leuchten.
#. Danach nähere ich mich dem ESP32 wieder.
#. Die Signalstärke sollte wieder steigen und weitere LEDs sollten
   eingeschaltet werden.


Erwartetes Verhalten
--------------------

Bei einer sehr guten Verbindung:

.. code-block:: text

   WiFi: 75 - 100 %

   LED1  ON
   LED2  ON
   LED3  ON
   LED4  ON


Bei einer guten Verbindung:

.. code-block:: text

   WiFi: 50 - 74 %

   LED1  ON
   LED2  ON
   LED3  ON
   LED4  OFF


Bei einer schwachen Verbindung:

.. code-block:: text

   WiFi: 25 - 49 %

   LED1  ON
   LED2  ON
   LED3  OFF
   LED4  OFF


Bei einer sehr schwachen Verbindung:

.. code-block:: text

   WiFi: 1 - 24 %

   LED1  ON
   LED2  OFF
   LED3  OFF
   LED4  OFF


Keine Verbindung:

.. code-block:: text

   WiFi: getrennt

   LED1  ON
   LED2  OFF
   LED3  OFF
   LED4  OFF


Überprüfung der YAML-Konfiguration
----------------------------------

Bevor ich die neue Konfiguration auf den ESP32 übertrage, überprüfe ich zuerst,
ob die YAML-Dateien von ESPHome korrekt erkannt werden.

Dafür verwende ich:

.. code-block:: powershell

   esphome config .\main.yaml

Dadurch kann ich Fehler in der YAML-Struktur oder fehlende IDs erkennen, bevor
das Programm kompiliert wird.


Programm auf den ESP32 übertragen
---------------------------------

Nach erfolgreicher Überprüfung kann ich die Konfiguration mit folgendem Befehl
kompilieren und auf den ESP32 übertragen:

.. code-block:: powershell

   esphome run .\main.yaml

Da mein ESP32 bereits mit meinem mobilen Hotspot verbunden ist, kann die neue
Konfiguration wieder über **OTA (Over the Air)** übertragen werden.


Live-Logs verwenden
-------------------

Während des Funktionstests kann ich zusätzlich die ESPHome-Logs anzeigen.

Dazu verwende ich:

.. code-block:: powershell

   esphome logs .\main.yaml

Damit kann ich kontrollieren, ob der ESP32 weiterhin mit meinem Hotspot
verbunden ist und welche Signalwerte vom WiFi-Sensor geliefert werden.


Test über den ESPHome-Webserver
-------------------------------

Zusätzlich kann ich den WiFi-Wert im ESPHome-Webinterface beobachten.

Dort sollte unter anderem der Sensor

.. code-block:: text

   WiFi Signal Percent

angezeigt werden.

Dadurch kann ich gleichzeitig vergleichen:

.. code-block:: text

   ESPHome-Webserver:

   WiFi Signal Percent: 82 %


   ESP32-Board:

   LED1  ON
   LED2  ON
   LED3  ON
   LED4  ON

Wenn beide Anzeigen zusammenpassen, funktioniert meine Zuordnung korrekt.


Mögliche Verbesserung
---------------------

Eine mögliche Erweiterung wäre, die Balkenanzeige nicht permanent laufen zu
lassen.

Beispielsweise könnte ich mit einem Taster zwischen verschiedenen
Anzeigemodi wechseln:

.. code-block:: text

   Modus 1:
   Temperaturanzeige

   Modus 2:
   WiFi-Qualitätsanzeige

Damit könnten dieselben vier LEDs für mehrere Funktionen verwendet werden.

Für diese Aufgabe beschränke ich mich jedoch auf die WiFi-Qualitätsanzeige,
damit die Funktion einfach getestet und im Video klar gezeigt werden kann.


Ergebnis
--------

Mit meiner zweiten eigenen Idee verwende ich die WLAN-Signalstärke nicht nur
als Wert im ESPHome-Webinterface, sondern stelle sie direkt am ESP32 dar.

Der ESP32 misst regelmässig die Qualität der Verbindung zu meinem mobilen
Hotspot.

Der gemessene dBm-Wert wird in einen Prozentwert umgerechnet und anschliessend
in vier Signalbereiche eingeteilt.

Je besser die Verbindung ist, desto mehr LEDs leuchten.

Dadurch entsteht aus den vier vorhandenen LEDs eine einfache
WiFi-Balkenanzeige.

Mit dem Projekt konnte ich mehrere Funktionen von ESPHome miteinander
kombinieren:

* einen internen Sensor auslesen,
* einen Messwert umrechnen,
* Bedingungen mit Lambda-Ausdrücken erstellen,
* vier Ausgänge abhängig von einem Sensorwert steuern,
* und den WLAN-Verbindungsstatus berücksichtigen.


Videonachweis
-------------

.. youtube:: CJ676sheN0g
   :width: 100%