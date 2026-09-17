Portfolio Möglichkeiten von ESPHome & HA
========================================

.. important::
   Sie haben sich über die Möglichkeiten von ESPHome und HomeAssistant informiert.
   Wo liegen die Grenzen, wie unterscheidet es sich von anderen Tools, welche Anderen Tools gibt es überhaupt? Wo liegen die Unterschiede?


ESPHome und Home Assistant
--------------------------

``ESPHome`` und ``Home Assistant`` gehören beide in den Bereich IoT und Smart Home, übernehmen aber unterschiedliche Aufgaben.

**ESPHome** läuft auf Mikrocontrollern wie einem ``ESP32`` oder ``ESP8266`` und verbindet die angeschlossene Hardware mit dem Netzwerk. Damit können Sensoren ausgelesen, Aktoren angesteuert und kleinere Automatisierungen direkt auf dem Mikrocontroller ausgeführt werden.

**Home Assistant** läuft dagegen als zentraler Smart-Home-Server. Dort können Geräte und Dienste verschiedener Hersteller zusammengeführt, visualisiert und automatisiert werden.

Vereinfacht sehe ich die Aufgabenteilung so:

``Sensor / Aktor → ESP32 mit ESPHome → Netzwerk → Home Assistant → Automatisierung``

.. note::
   Für mich ist der wichtigste Unterschied: **ESPHome befindet sich nahe an der Hardware, Home Assistant verbindet und automatisiert ganze Systeme.**


Möglichkeiten von ESPHome
-------------------------

Mit ``ESPHome`` kann beispielsweise ein ``ESP32`` oder ``ESP8266`` über eine YAML-Konfiguration für verschiedene Sensoren und Aktoren eingerichtet werden.

Im Modul verwenden wir dafür ein Acebott-Board mit einem HAT. Dadurch können verschiedene Komponenten angeschlossen und ausprobiert werden, ohne für jede kleine Übung eine umfangreiche Verkabelung aufzubauen.

Die Konfiguration wird beispielsweise in einer Datei wie ``main.yaml`` beschrieben und anschliessend für den Mikrocontroller kompiliert.

ESPHome bietet unter anderem folgende Möglichkeiten:

* Sensorwerte wie Temperatur oder Luftfeuchtigkeit auslesen
* LEDs und andere Aktoren ansteuern
* Displays verwenden
* Geräte über WLAN in das Netzwerk integrieren
* eine Weboberfläche für ein Gerät bereitstellen
* Geräte direkt in Home Assistant integrieren
* einfache Logik direkt auf dem Mikrocontroller ausführen
* spätere Änderungen über ``OTA`` (*Over the Air*) übertragen

.. tip::
   Ein Vorteil von ESPHome ist für mich, dass für viele typische IoT-Aufgaben nicht zuerst ein komplettes Programm von Grund auf geschrieben werden muss. Viele Funktionen können über eine YAML-Konfiguration zusammengesetzt werden.


Grenzen von ESPHome
-------------------

ESPHome kann selbst Logik ausführen, diese läuft jedoch auf einem vergleichsweise kleinen Mikrocontroller.

Für einfache lokale Aufgaben ist das sinnvoll:

``Temperatur messen → Grenzwert prüfen → LED einschalten``

Sobald jedoch mehrere Geräte, unterschiedliche Hersteller oder umfangreichere Automatisierungen miteinander verbunden werden sollen, wird ein zentrales System interessanter.

Ein ESP könnte beispielsweise problemlos seine eigene Temperatur messen und darauf reagieren. Wenn aber gleichzeitig Wetterdaten, Beleuchtung, Heizung, Bewegungsmelder und Geräte verschiedener Hersteller berücksichtigt werden sollen, ist ein Smart-Home-Server wie Home Assistant besser geeignet.

ESPHome ersetzt deshalb für mich **keinen vollständigen Smart-Home-Server**. Seine Stärke liegt vor allem darin, Mikrocontroller und deren Sensoren und Aktoren einfach in ein vernetztes System einzubinden.


Möglichkeiten von Home Assistant
--------------------------------

``Home Assistant`` übernimmt eine andere Rolle. Es ist ein zentraler Smart-Home-Server, in dem Geräte und Dienste zusammengeführt werden können.

Ein grosser Vorteil ist, dass nicht alle Geräte vom gleichen Hersteller stammen müssen. Unterschiedliche Systeme können über ihre jeweiligen Integrationen gemeinsam verwendet werden.

Home Assistant kann beispielsweise:

* Geräte und Sensorwerte zentral verwalten
* Werte über Dashboards darstellen
* Automatisierungen ausführen
* Geräte verschiedener Hersteller miteinander verbinden
* ESPHome-Geräte integrieren
* weitere Systeme und Dienste einbinden

Dadurch kann die Logik von einem einzelnen ESP auf ein übergeordnetes System verlagert werden.

Ein einfaches Beispiel wäre:

``Bewegungsmelder → ESPHome → Home Assistant → Licht einschalten``

Home Assistant könnte dabei zusätzlich Informationen von anderen Geräten berücksichtigen:

``Bewegung erkannt + nach Sonnenuntergang + niemand schläft → Licht einschalten``

Genau hier sehe ich einen grossen Unterschied zu einer einfachen Logik direkt auf dem ESP. Home Assistant kann Informationen aus **mehreren Geräten und Diensten** zusammenführen und daraus gemeinsame Automatisierungen erstellen.


ESPHome und Home Assistant zusammen
-----------------------------------

ESPHome und Home Assistant sind deshalb für mich weniger Konkurrenten als zwei Werkzeuge, die sich gut ergänzen.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * -
     - ``ESPHome``
     - ``Home Assistant``
   * - **Aufgabe**
     - Mikrocontroller konfigurieren und Hardware ansteuern
     - Geräte und Dienste zentral verbinden
   * - **Läuft auf**
     - beispielsweise ``ESP32`` oder ``ESP8266``
     - Smart-Home-Server
   * - **Nähe zur Hardware**
     - hoch
     - geringer
   * - **Sensoren / Aktoren**
     - direkt am Mikrocontroller
     - über integrierte Geräte und Systeme
   * - **Automatisierungen**
     - lokale und gerätenahe Logik
     - geräteübergreifende Automatisierungen
   * - **Oberfläche**
     - einfache Weboberfläche möglich
     - umfangreiche zentrale Dashboards
   * - **Stärke**
     - eigene IoT-Hardware einfach integrieren
     - unterschiedliche Systeme zusammenführen

Ein selbstgebauter Temperatursensor könnte beispielsweise mit ESPHome betrieben werden. Home Assistant könnte dessen Messwerte anschliessend gemeinsam mit einer smarten Heizung, Fensterkontakten und weiteren Geräten für eine Automatisierung verwenden.


Grenzen von Home Assistant
--------------------------

Auch Home Assistant hat Grenzen. Für das direkte Programmieren eines Mikrocontrollers und dessen Hardware ist Home Assistant nicht gedacht. Dafür benötigt man beispielsweise ESPHome oder eine andere Firmware.

Ausserdem braucht Home Assistant ein System, auf dem der Server dauerhaft läuft. Im Unterricht wurde dafür beispielsweise ein ``Raspberry Pi`` genannt. Alternativ kann Home Assistant auch virtualisiert betrieben werden.

Mit der Anzahl der eingebundenen Geräte, Integrationen und Automatisierungen kann auch die Komplexität des gesamten Systems steigen. Ein Fehler in einer zentralen Automatisierung kann dadurch mehrere Geräte betreffen.

Eine weitere Grenze können die Geräte selbst darstellen. Nicht jedes Smart-Home-Gerät besitzt eine offene oder lokale Schnittstelle. Manche Produkte sind von einer Hersteller-Cloud abhängig. Auch Home Assistant kann eine solche Abhängigkeit nicht in jedem Fall vollständig entfernen.

.. warning::
   Je mehr Geräte und Hersteller in einem Smart Home miteinander verbunden werden, desto wichtiger werden **IT-Sicherheit, Datenschutz, Updates und die Zuverlässigkeit des zentralen Systems**.


Andere Tools und Möglichkeiten
------------------------------

ESPHome und Home Assistant sind nicht die einzigen Werkzeuge im IoT- und Smart-Home-Bereich. Je nach Aufgabe gibt es andere Lösungen mit unterschiedlichen Schwerpunkten.


Arduino
~~~~~~~

Ein ``ESP32`` kann beispielsweise klassisch mit dem Arduino-Framework beziehungsweise C/C++ programmiert werden.

Damit hat man sehr viel Kontrolle über das eigene Programm und kann die Logik selbst implementieren. Dafür muss allerdings auch wesentlich mehr selbst programmiert werden.

Der Unterschied zu ESPHome liegt für mich hauptsächlich im Ansatz:

``ESPHome → Funktionen konfigurieren``

``Arduino → Verhalten selbst programmieren``

Für spezielle Anwendungen kann die direkte Programmierung mehr Freiheit bieten. Für typische Sensoren, Aktoren und Smart-Home-Anwendungen kann ESPHome dagegen schneller zum Ziel führen.


Tasmota
~~~~~~~

``Tasmota`` ist eine weitere Firmware für ESP-basierte IoT-Geräte. Sie kann verwendet werden, um kompatible Smart-Home-Geräte lokal zu betreiben und in andere Systeme einzubinden.

Im Vergleich zu ESPHome liegt der Fokus stärker auf einer bereits fertigen Firmware, die anschliessend konfiguriert wird. ESPHome erstellt dagegen anhand der YAML-Konfiguration eine auf das jeweilige Gerät zugeschnittene Firmware.

Vereinfacht sehe ich den Unterschied so:

``Tasmota → vorhandene Firmware konfigurieren``

``ESPHome → eigene Gerätekonfiguration als Firmware erstellen``

Für eigene Projekte mit individuell angeschlossenen Sensoren und Aktoren finde ich den Ansatz von ESPHome interessant. Tasmota kann dagegen eine Möglichkeit sein, kompatible bestehende Geräte lokal in ein Smart-Home-System einzubinden.


Node-RED
~~~~~~~~

``Node-RED`` verfolgt wiederum einen anderen Ansatz. Abläufe werden grafisch als sogenannte Flows aufgebaut.

Damit eignet es sich besonders dafür, Daten und Ereignisse zwischen verschiedenen Systemen zu verarbeiten und daraus Automatisierungen aufzubauen.

Node-RED kann auch zusammen mit Home Assistant eingesetzt werden. Es ist deshalb nicht zwingend ein Ersatz für Home Assistant, sondern kann dessen Möglichkeiten bei komplexeren Abläufen ergänzen.


MQTT und Mosquitto
~~~~~~~~~~~~~~~~~~

``MQTT`` unterscheidet sich von den bisherigen Werkzeugen, da es keine vollständige Smart-Home-Plattform und auch keine Firmware ist. Es handelt sich um ein **Kommunikationsprotokoll**.

Geräte können Nachrichten zu bestimmten Topics veröffentlichen (*publish*) und andere Systeme können diese Topics abonnieren (*subscribe*).

Dazwischen befindet sich ein MQTT-Broker. Eine bekannte Möglichkeit dafür ist ``Mosquitto``.

Ein vereinfachtes Beispiel:

``Temperatursensor → MQTT → Mosquitto Broker → Home Assistant``

MQTT ist besonders interessant, wenn unterschiedliche Geräte oder Systeme miteinander kommunizieren sollen und beispielsweise keine direkte Integration in Home Assistant vorhanden ist.

.. note::
   ``MQTT`` und ``Mosquitto`` sollte man dabei unterscheiden: **MQTT ist das Protokoll**, während **Mosquitto ein MQTT-Broker** ist, der die Nachrichten zwischen den Teilnehmern vermittelt.


Unterschiede im Überblick
-------------------------

Die verschiedenen Werkzeuge lösen nicht alle dasselbe Problem. Sie befinden sich teilweise sogar auf unterschiedlichen Ebenen eines IoT-Systems.

.. list-table::
   :header-rows: 1
   :widths: 20 35 45

   * - Werkzeug
     - Schwerpunkt
     - Typischer Einsatz
   * - ``ESPHome``
     - Mikrocontroller und Hardware
     - Sensoren und Aktoren mit einem ESP verbinden
   * - ``Home Assistant``
     - Zentrale Smart-Home-Plattform
     - Geräte verbinden, visualisieren und automatisieren
   * - ``Arduino``
     - Direkte Programmierung
     - Individuelle Firmware und spezielle Hardwarelogik
   * - ``Tasmota``
     - IoT-Firmware
     - Kompatible ESP-Geräte lokal betreiben und integrieren
   * - ``Node-RED``
     - Grafische Abläufe
     - Datenflüsse und Automatisierungen erstellen
   * - ``MQTT``
     - Kommunikationsprotokoll
     - Nachrichten zwischen unterschiedlichen Systemen austauschen
   * - ``Mosquitto``
     - MQTT-Broker
     - MQTT-Nachrichten zwischen Teilnehmern vermitteln


Was ich daraus mitnehme
-----------------------

Für mich wurde vor allem klar, dass **ESPHome und Home Assistant unterschiedliche Ebenen eines IoT-Systems abdecken**.

ESPHome macht es relativ einfach, eigene Hardware mit einem ``ESP32`` in das Netzwerk zu bringen. Sensoren und Aktoren können konfiguriert und bereits mit lokaler Logik versehen werden.

Home Assistant setzt eine Ebene darüber an. Dort können diese ESPHome-Geräte mit weiteren Geräten und Diensten verbunden werden. Dadurch entstehen Automatisierungen, die nicht mehr nur ein einzelnes Gerät betreffen.

Die anderen Werkzeuge zeigen gleichzeitig, dass es nicht nur einen möglichen Weg gibt. Mit Arduino hat man mehr Kontrolle über die eigentliche Programmierung. Tasmota bietet einen anderen Ansatz für ESP-basierte Geräte. Node-RED ermöglicht grafische Abläufe und MQTT stellt eine Möglichkeit zur Kommunikation zwischen unterschiedlichen Systemen bereit.

Ich würde deshalb nicht sagen, dass eines dieser Werkzeuge grundsätzlich das beste ist. Entscheidend ist, **welches Problem gelöst werden soll und auf welcher Ebene des IoT-Systems man arbeitet**.

.. note::
   Für unser Modul finde ich die Kombination aus ``ESPHome`` und ``Home Assistant`` sinnvoll: Mit ESPHome können wir zuerst verstehen und ausprobieren, wie Sensoren und Aktoren an einem ESP funktionieren. Home Assistant zeigt anschliessend, wie aus mehreren einzelnen Geräten ein gemeinsames und automatisiertes System entstehen kann.