Portfolio Sensoren und Aktoren
==============================

.. important::
   Sie kennen verschiedene Sensoren und Aktoren. Was ist der Unterschied? Sie können dies in eigenen Worten erläutern.


Sensoren und Aktoren
--------------------

Sensoren und Aktoren bilden für mich die Verbindung zwischen der **physischen und der digitalen Welt**. Der Unterschied liegt hauptsächlich darin, in welche Richtung Informationen fliessen.

Ein **Sensor** nimmt etwas aus seiner Umgebung wahr und wandelt diese physikalische Grösse in einen Wert um, den ein digitales System weiterverarbeiten kann.

Ein **Aktor** funktioniert in die andere Richtung. Er erhält ein elektrisches Signal von einem System und setzt dieses wieder in eine physische Aktion um.

Ich kann mir den Unterschied deshalb einfach so merken:

``Sensor: reale Welt → Daten``

``Aktor: Daten / Signal → reale Welt``

.. note::
   Ein guter Vergleich aus dem Unterricht ist der menschliche Körper. Unsere **Augen, Ohren und anderen Sinne** funktionieren ähnlich wie Sensoren, da sie Informationen aus der Umgebung aufnehmen. Unsere **Muskeln** oder der Mund beim Sprechen funktionieren eher wie Aktoren, da damit eine Aktion ausgeführt wird.


Sensoren
--------

Sensoren können sehr unterschiedliche physikalische Grössen erfassen. Je nachdem, was ein System über seine Umgebung wissen muss, wird ein anderer Sensortyp benötigt.

Beispiele dafür sind:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Sensortyp
     - Was wird erfasst?
   * - Temperatursensor
     - Temperatur
   * - Feuchtigkeitssensor
     - Luft- oder Materialfeuchtigkeit
   * - Drucksensor
     - Luft- oder anderer physikalischer Druck
   * - Bewegungsmelder
     - Bewegung in der Umgebung
   * - Näherungssensor
     - Ob sich ein Objekt in der Nähe befindet
   * - Helligkeitssensor
     - Licht beziehungsweise Helligkeit
   * - Beschleunigungssensor
     - Beschleunigung und Bewegungsänderungen
   * - Gas-Sensor
     - Bestimmte Gase beziehungsweise Veränderungen der Luft

Wichtig ist dabei, dass ein Sensor die physikalische Grösse nicht einfach nur erkennt, sondern daraus einen **maschinenlesbaren Wert** erzeugt, mit dem anschliessend weitergearbeitet werden kann.

Im Unterricht wurde auch angesprochen, dass bei der Auswahl eines Sensors besonders **Genauigkeit und Zuverlässigkeit** wichtig sind. Ein günstiger Sensor reicht möglicherweise für ein einfaches Hobbyprojekt aus, während bei einer kritischen Anwendung wesentlich höhere Anforderungen an die Messwerte gestellt werden.


Umgebungssensoren aus dem Unterricht
------------------------------------

Im Modul arbeiten wir unter anderem mit den Umgebungssensoren ``BMP280``, ``BME280`` und ``BME680``. An diesen drei Sensoren sieht man gut, dass ähnlich aussehende Bauteile unterschiedliche Mengen an Informationen über ihre Umgebung erfassen können.

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Sensor
     - Messgrössen
     - Schnittstelle
   * - ``BMP280``
     - Temperatur und Luftdruck
     - ``I2C`` / ``SPI``
   * - ``BME280``
     - Temperatur, Luftdruck und relative Luftfeuchtigkeit
     - ``I2C`` auf unserem Breakout
   * - ``BME680``
     - Temperatur, Luftdruck, Luftfeuchtigkeit und Luftgüte
     - ``I2C`` / ``SPI``

Beim ``BMP280`` fand ich interessant, wie genau der Luftdruck gemessen werden kann. Laut Unterricht erreicht der Sensor ungefähr ``±1 Pa`` Genauigkeit. Dadurch können sogar sehr kleine Höhenunterschiede erkannt werden.

Der ``BME280`` erweitert diese Messmöglichkeiten zusätzlich um die **relative Luftfeuchtigkeit**. Das ``E`` in der Bezeichnung steht dabei für *Environmental*.

Eine Besonderheit des ``BME680`` ist die Messung der **Luftgüte**. Dafür besitzt der Sensor eine kleine interne Heizung. Diese Heizung kann wiederum die Temperaturmessung beeinflussen. Werden viele Messungen in kurzer Zeit durchgeführt, kann der gemessene Temperaturwert laut Unterricht um bis zu ungefähr ``1.5 °C`` höher liegen.

.. tip::
   Gerade der ``BME680`` zeigt für mich, dass man Sensorwerte nicht einfach blind übernehmen sollte. Es ist auch wichtig zu verstehen, **wie ein Sensor misst und wodurch seine Messung beeinflusst werden kann**.


Aktoren
-------

Aktoren machen im Prinzip das Gegenteil eines Sensors. Sie messen keine Eigenschaft der Umgebung, sondern **führen eine Aktion aus**.

Beispiele für Aktoren sind:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Aktor
     - Physische Ausgabe
   * - LED / Lampe
     - Licht
   * - Motor
     - Bewegung
   * - Servo
     - Gezielte mechanische Bewegung
   * - Lautsprecher / Glocke
     - Schall
   * - Elektromagnet
     - Magnetische beziehungsweise mechanische Wirkung

Im Unterricht arbeiten wir hauptsächlich mit **LEDs** als Aktoren. Das ist praktisch, weil man sofort sehen kann, ob eine vom System ausgelöste Aktion funktioniert.


Zusammenspiel in einem IoT-System
---------------------------------

Besonders interessant wird es, wenn Sensor und Aktor miteinander kombiniert werden.

Ein Sensor könnte beispielsweise die Temperatur messen. Ein ``ESP32`` verarbeitet den Messwert und entscheidet anhand einer programmierten Logik, ob ein Aktor eingeschaltet werden soll.

``Temperatursensor → ESP32 → Logik → Aktor``

Ein einfaches Beispiel wäre:

``Temperatur zu hoch → Lüfter einschalten``

Der Sensor liefert dabei nur die Information. Die Verarbeitung entscheidet, **was mit dieser Information passieren soll**, und der Aktor setzt die Entscheidung schliesslich in der physischen Welt um.


Was ich daraus mitnehme
-----------------------

Für mich ist der wichtigste Unterschied zwischen Sensor und Aktor die **Richtung zwischen physischer und digitaler Welt**.

Ein Sensor macht einen Zustand der realen Welt für Software messbar. Ein Aktor ermöglicht es der Software dagegen, wieder etwas in der realen Welt zu bewirken.

``Sensor → erfassen``

``Aktor → ausführen``

Erst durch die Verarbeitung dazwischen kann daraus eine automatische Funktion entstehen. Genau dieses Zusammenspiel ist für IoT interessant: Ein System kann seine Umgebung **wahrnehmen, die Daten verarbeiten und anschliessend darauf reagieren**.