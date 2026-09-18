Video wechseln der LED nach Temp
================================

.. important::
   Programm aus 4.1 zum wechseln der LED nach Temp und Anzeige der Temp


Aufgabe
-------

Für diese Aufgabe soll die aktuell gemessene Temperatur bestimmen, welche LED
auf dem ESP32-Board leuchtet. Zusätzlich soll die gemessene Temperatur auf der
vorhandenen Anzeige des Boards dargestellt werden.

Die vorgegebenen Temperaturbereiche sind:

.. list-table::
   :header-rows: 1
   :widths: 35 30 25

   * - Temperatur
     - LED
     - LED-ID
   * - Unter 20 °C
     - Blau
     - ``LED3``
   * - 20 °C bis unter 23 °C
     - Grün
     - ``LED2``
   * - 23 °C bis 25 °C
     - Gelb
     - ``LED4``
   * - Über 25 °C
     - Rot
     - ``LED1``


Vorhandenes LED-Mapping
-----------------------

Die Zuordnung der LEDs hatte ich bereits bei den vorherigen Übungen am Board
überprüft:

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
     - Gelb
     - ``GPIO12``


Temperatursensor
----------------

Für die Temperaturmessung verwende ich den bereits vorhandenen DHT-Sensor des
Demo-Projekts. Dieser ist an ``GPIO16`` angeschlossen. Der Temperaturwert besitzt
in ESPHome die ID ``temperatur``. Dadurch kann ich denselben Messwert sowohl für
die LED-Steuerung als auch für die Temperaturanzeige verwenden.

Beim Test ist mir aufgefallen, dass die Temperatur des DHT-Sensors zu hoch
angezeigt wurde und dass sich der Messwert relativ langsam aktualisierte.

Aus diesem Grund habe ich zwei Anpassungen vorgenommen:

* Das ``update_interval`` wurde auf ``2s`` reduziert.
* Auf den Temperaturwert wird ein Offset von ``-2.0 °C`` angewendet.

Der DHT-Sensor liefert dadurch alle zwei Sekunden einen neuen Messwert. Die
LED-Steuerung und die Anzeige können entsprechend schneller auf eine
Temperaturänderung reagieren.

Der Offset dient dazu, eine konstante Abweichung des Sensors zu korrigieren.
Der Wert von ``-2.0`` bedeutet, dass vom gemessenen Rohwert 2 °C abgezogen
werden.

Der Offset sollte bei Bedarf mit einem zuverlässigen Vergleichsthermometer
überprüft werden. Falls der DHT-Sensor beispielsweise weiterhin konstant zu
hoch misst, kann der Offset entsprechend angepasst werden.

Zusätzlich muss darauf geachtet werden, dass sich der DHT-Sensor nicht direkt
neben einer Wärmequelle befindet. Der ESP32, Spannungsregler oder andere
elektronische Komponenten können sich während des Betriebs erwärmen und dadurch
die Temperaturmessung beeinflussen.


``dht.yaml``
~~~~~~~~~~~~

.. code-block:: yaml

   sensor:
     - platform: dht
       model: AUTO_DETECT

       temperature:
         id: "temperatur"
         name: "Sensor dht Temperature"
         icon: "mdi:thermometer-lines"
         device_class: "temperature"
         state_class: "measurement"
         filters:
           - offset: -2.0

       humidity:
         name: "Sensor dht Humidity"
         icon: "mdi:water-percent"

       update_interval: 2s

       pin:
         number: GPIO16


Temperaturabhängige LED-Steuerung
---------------------------------

Für die Steuerung der LEDs habe ich eine eigene Datei
``temperature_led.yaml`` erstellt. Dadurch bleibt die ``main.yaml``
übersichtlich und die Logik für diese Aufgabe befindet sich in einer eigenen
Datei.

Die Steuerung überprüft jede Sekunde den zuletzt gemessenen Temperaturwert.
Der DHT-Sensor selbst liefert alle zwei Sekunden einen neuen Messwert.

Zuerst werden alle vier LEDs ausgeschaltet. Anschliessend wird anhand des
aktuellen Temperaturbereichs genau die passende LED eingeschaltet.

Dadurch kann immer nur eine der vier Temperatur-LEDs gleichzeitig leuchten.


``temperature_led.yaml``
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # Temperaturabhaengige LED-Steuerung
   #
   # LED1 = Rot
   # LED2 = Gruen
   # LED3 = Blau
   # LED4 = Gelb
   #
   # Unter 20 C        -> Blau
   # 20 C bis < 23 C   -> Gruen
   # 23 C bis <= 25 C  -> Gelb
   # Ueber 25 C        -> Rot

   interval:
     - interval: 1s
       then:

         # Alle LEDs zuerst ausschalten
         - switch.turn_off: LED1
         - switch.turn_off: LED2
         - switch.turn_off: LED3
         - switch.turn_off: LED4

         # Unter 20 C -> Blau
         - if:
             condition:
               lambda: |-
                 return !isnan(id(temperatur).state) &&
                        id(temperatur).state < 20.0;
             then:
               - switch.turn_on: LED3

         # 20 C bis unter 23 C -> Gruen
         - if:
             condition:
               lambda: |-
                 return !isnan(id(temperatur).state) &&
                        id(temperatur).state >= 20.0 &&
                        id(temperatur).state < 23.0;
             then:
               - switch.turn_on: LED2

         # 23 C bis einschliesslich 25 C -> Gelb
         - if:
             condition:
               lambda: |-
                 return !isnan(id(temperatur).state) &&
                        id(temperatur).state >= 23.0 &&
                        id(temperatur).state <= 25.0;
             then:
               - switch.turn_on: LED4

         # Ueber 25 C -> Rot
         - if:
             condition:
               lambda: |-
                 return !isnan(id(temperatur).state) &&
                        id(temperatur).state > 25.0;
             then:
               - switch.turn_on: LED1


Temperatur auf der Anzeige
--------------------------

Auf meinem Board ist bereits eine vierstellige TM1637-Anzeige vorhanden.
Diese wurde im Demo-Projekt bisher verwendet, um die aktuelle Uhrzeit
anzuzeigen.

Für diese Aufgabe ändere ich die Anzeige so, dass anstelle der Uhrzeit die
aktuell vom DHT-Sensor gemessene Temperatur dargestellt wird.

Die Anzeige ist über ``GPIO18`` und ``GPIO17`` mit dem ESP32 verbunden.

Da sie vier Stellen besitzt, kann beispielsweise eine Temperatur wie
``27.5`` direkt dargestellt werden.

Die Anzeige wird häufiger aktualisiert als der DHT-Sensor. Dadurch wird ein
neuer Temperaturwert unmittelbar auf dem Display dargestellt, sobald ESPHome
eine neue Messung erhalten hat.

Falls noch kein gültiger Temperaturwert vorhanden ist, werden vier Striche
angezeigt.


``tm1637.yaml``
~~~~~~~~~~~~~~~

.. code-block:: yaml

   display:
     - platform: tm1637
       id: tm1637_display
       clk_pin: GPIO18
       dio_pin: GPIO17
       inverted: false
       length: 4
       update_interval: 500ms

       lambda: |-
         if (isnan(id(temperatur).state)) {
           it.print("----");
         } else {
           it.printf(0, "%.1f", id(temperatur).state);
         }


Nicht verwendetes LCD
---------------------

Im Demo-Projekt existiert zusätzlich die Datei ``lcd_pcf8574.yaml`` für ein
separates I2C-LCD. Beim ersten Versuch hatte ich dieses Display ebenfalls
aktiviert.

In den Live-Logs von ESPHome wurde jedoch folgende Fehlermeldung angezeigt:

.. code-block:: text

   [E][lcd_pcf8574:029]: Communication failed
   [E][component:188]: display is marked FAILED: unspecified

Damit konnte ich erkennen, dass dieses separate LCD bei meinem aktuellen
Aufbau nicht erreichbar ist.

Für die Aufgabe verwende ich deshalb die vorhandene TM1637-Anzeige und
deaktiviere ``lcd_pcf8574.yaml`` wieder in der ``main.yaml``.

Dadurch wird verhindert, dass ESPHome ständig versucht, ein nicht vorhandenes
Display anzusprechen.


LED-Konfiguration
-----------------

Die vier LEDs sind bereits in der Datei ``led.yaml`` definiert. Diese
Konfiguration bleibt unverändert und wird von der Temperatursteuerung
verwendet.


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


Anpassung der ``main.yaml``
---------------------------

In der ``main.yaml`` habe ich die neue Datei ``temperature_led.yaml``
eingebunden.

Die vorhandene ``tm1637.yaml`` bleibt ebenfalls aktiviert, enthält nun aber
die Temperaturanzeige anstelle der Zeitanzeige.

Das separate ``lcd_pcf8574.yaml`` wird nicht eingebunden, da dieses Display
bei meinem aktuellen Aufbau nicht erreichbar ist.

Die bereits vorhandenen Komponenten des Demo-Projekts bleiben bestehen. Auch
meine zuvor erstellte Self-Destruct-Sequenz bleibt weiterhin eingebunden.


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

     on_connect:
       then:
         - switch.turn_on:
             id: LED2

         - switch.turn_off:
             id: LED1

     on_disconnect:
       then:
         - switch.turn_on:
             id: LED1

         - switch.turn_off:
             id: LED2

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
     # sda: 4
     # scl: 5

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

     # Include the temperature dependent LED control
     temperature_led: !include temperature_led.yaml

     # LCD is not used with my current hardware setup
     #lcd: !include lcd_pcf8574.yaml

     # Include the FastLED configuration
     #fastled: !include fastled.yaml


Zusammenspiel der Komponenten
-----------------------------

Die einzelnen YAML-Dateien erfüllen jeweils eine bestimmte Aufgabe.

``dht.yaml``
   Liest die Temperatur und Luftfeuchtigkeit vom DHT-Sensor ein.

``temperature_led.yaml``
   Prüft die aktuelle Temperatur und schaltet abhängig vom Temperaturbereich
   die entsprechende LED ein.

``tm1637.yaml``
   Zeigt den aktuellen Temperaturwert auf der vierstelligen Anzeige an.

``led.yaml``
   Definiert die vier verwendeten LEDs und deren GPIO-Anschlüsse.

``main.yaml``
   Enthält die Grundkonfiguration des ESP32 und bindet die einzelnen
   Konfigurationsdateien als Packages ein.

Der Ablauf sieht damit vereinfacht folgendermassen aus:

.. code-block:: text

   DHT-Sensor
       |
       v
   Temperaturmessung
       |
       +--------------------+
       |                    |
       v                    v
   LED-Steuerung        TM1637-Anzeige
       |                    |
       v                    v
   passende LED         Temperaturwert


Aktualisierungszeiten
---------------------

Die einzelnen Komponenten besitzen unterschiedliche Aktualisierungszeiten.

Der DHT-Sensor misst die Temperatur alle ``2s``:

.. code-block:: yaml

   update_interval: 2s

Die LED-Steuerung überprüft jede Sekunde den zuletzt verfügbaren Messwert:

.. code-block:: yaml

   interval:
     - interval: 1s

Die TM1637-Anzeige wird alle ``500ms`` aktualisiert:

.. code-block:: yaml

   update_interval: 500ms

Die schnellere Aktualisierung von LED-Steuerung und Display bedeutet nicht,
dass der DHT-Sensor häufiger misst. Ein neuer Temperaturwert entsteht weiterhin
alle zwei Sekunden.

Dadurch wird der Sensor nicht unnötig schnell abgefragt, während die restliche
Steuerung trotzdem schnell auf einen neuen Messwert reagieren kann.


Korrektur der Temperaturmessung
-------------------------------

Beim Test ist aufgefallen, dass die vom DHT-Sensor angezeigte Temperatur zu
hoch sein kann.

In ESPHome kann eine konstante Abweichung mit einem Filter korrigiert werden:

.. code-block:: yaml

   filters:
     - offset: -2.0

Mit dieser Einstellung werden vom gemessenen Wert 2 °C abgezogen.

Beispiel:

.. code-block:: text

   Rohwert des Sensors:     26.0 °C
   Offset:                  -2.0 °C
   Angezeigter Wert:        24.0 °C

Der Offset sollte jedoch nicht beliebig gewählt werden. Für eine genaue
Kalibrierung muss der DHT-Sensor mit einem zuverlässigen Thermometer verglichen
werden.

Die benötigte Korrektur kann grundsätzlich nach folgendem Prinzip bestimmt
werden:

.. code-block:: text

   Offset = Referenztemperatur - gemessene Temperatur

Beispiel:

.. code-block:: text

   DHT-Sensor:             27.0 °C
   Referenzthermometer:    24.5 °C

   Offset = 24.5 - 27.0
   Offset = -2.5 °C

In diesem Beispiel wäre somit folgender Wert sinnvoll:

.. code-block:: yaml

   filters:
     - offset: -2.5

Für meine aktuelle Konfiguration verwende ich weiterhin ``-2.0``. Falls sich
bei einem Vergleich mit einem Referenzthermometer eine andere konstante
Abweichung zeigt, kann dieser Wert entsprechend angepasst werden.


Einfluss der Hardware auf die Messung
-------------------------------------

Nicht jede zu hohe Temperaturanzeige muss durch eine falsche Kalibrierung
entstehen.

Auch die Position des Sensors kann die Messung beeinflussen.

Der ESP32 sowie weitere elektronische Bauteile erzeugen während des Betriebs
Wärme. Befindet sich der DHT-Sensor direkt neben dem ESP32 oder einem
Spannungsregler, kann er dadurch eine höhere Temperatur messen als tatsächlich
im Raum vorhanden ist.

Für eine möglichst zuverlässige Messung sollte deshalb:

* der DHT-Sensor etwas Abstand zum ESP32 besitzen,
* der Sensor nicht direkt über einem warmen Bauteil montiert sein,
* Luft um den Sensor zirkulieren können,
* direkte Sonneneinstrahlung vermieden werden.

Erst nachdem diese Punkte überprüft wurden, sollte ein grösserer Software-Offset
verwendet werden.


Konfiguration überprüfen
-------------------------

Nachdem ich die Dateien angepasst habe, überprüfe ich zuerst die komplette
ESPHome-Konfiguration.

Dazu verwende ich im Projektordner folgenden Befehl:

.. code-block:: powershell

   esphome config .\main.yaml

Beim ersten Versuch wurde bereits ein Fehler in der Verschachtelung meiner
``if``-Bedingungen erkannt. Dadurch konnte ich diesen Fehler vor dem
Kompilieren und Übertragen auf den ESP32 korrigieren.

Beim Test mit dem zusätzlich aktivierten I2C-LCD konnte ich später über die
Live-Logs ebenfalls erkennen, dass die Kommunikation mit diesem Display
fehlschlug.

Deshalb verwende ich für die Temperaturanzeige die vorhandene TM1637-Anzeige.

Die Warnung zu ``GPIO12`` betrifft die bereits vorhandene ``LED4``. Für diese
Übung verwende ich weiterhin die vorgegebene Hardwarebelegung des Boards.


Programm auf den ESP32 übertragen
---------------------------------

Nach erfolgreicher Konfigurationsprüfung übertrage ich das Programm mit:

.. code-block:: powershell

   esphome run .\main.yaml

Da mein ESP32 bereits mit meinem iPhone-Hotspot verbunden ist, kann ich die
aktualisierte Konfiguration OTA (Over the Air) übertragen.

Nach der Übertragung kann ich die Live-Logs weiter beobachten und dadurch
kontrollieren, welche Temperatur der DHT-Sensor misst und welche LED von der
Steuerung eingeschaltet wird.

Die Logs können ebenfalls direkt mit folgendem Befehl geöffnet werden:

.. code-block:: powershell

   esphome logs .\main.yaml

Dadurch kann ich beobachten, ob alle zwei Sekunden ein neuer Temperaturwert
vom DHT-Sensor empfangen wird.


Funktionstest
-------------

Nach der Übertragung teste ich die verschiedenen Temperaturbereiche. Dabei
kontrolliere ich gleichzeitig die LEDs und den auf der TM1637-Anzeige
dargestellten Temperaturwert.

Das erwartete Verhalten ist:

* Unter 20 °C leuchtet die blaue LED.
* Von 20 °C bis unter 23 °C leuchtet die grüne LED.
* Von 23 °C bis 25 °C leuchtet die gelbe LED.
* Über 25 °C leuchtet die rote LED.
* Auf der TM1637-Anzeige wird gleichzeitig die aktuelle Temperatur angezeigt.
* Der DHT-Sensor liefert ungefähr alle zwei Sekunden einen neuen Messwert.

Bei einem ersten Test wurde beispielsweise eine Temperatur von ungefähr
``27.5 °C`` gemessen.

Damit liegt die Temperatur über 25 °C und entsprechend wurde ``LED1`` (Rot)
eingeschaltet.

Da die Temperaturmessung zunächst zu hoch erschien, verwende ich zusätzlich
den Offset von ``-2.0 °C`` und überprüfe den Messwert bei Bedarf mit einem
Referenzthermometer.

Für den vollständigen Funktionstest verändere ich die Temperatur am Sensor und
beobachte, ob beim Überschreiten der Grenzwerte automatisch auf die jeweils
richtige LED gewechselt wird.


Erwartetes Ergebnis
-------------------

Nach erfolgreicher Konfiguration arbeitet das System folgendermassen:

.. list-table::
   :header-rows: 1
   :widths: 35 30 30

   * - Temperatur
     - aktive LED
     - Anzeige
   * - Unter 20 °C
     - Blau
     - aktuelle Temperatur
   * - 20 °C bis unter 23 °C
     - Grün
     - aktuelle Temperatur
   * - 23 °C bis 25 °C
     - Gelb
     - aktuelle Temperatur
   * - Über 25 °C
     - Rot
     - aktuelle Temperatur

Damit erfüllt das Programm den Auftrag, die LED abhängig von der gemessenen
Temperatur zu wechseln und gleichzeitig die aktuelle Temperatur auf der
vorhandenen Anzeige darzustellen.


Videonachweis
-------------

.. youtube:: ij0IY__qH0Y
   :width: 100%