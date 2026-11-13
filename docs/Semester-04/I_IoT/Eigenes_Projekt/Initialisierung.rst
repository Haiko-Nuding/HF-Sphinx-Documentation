Initialisierungsbericht – Smart Window
======================================

:Autor: Haiko Nuding
:Modul: IoT – Semester 04
:Datum: 13.11.2026
:Status: Initialisierung zur Freigabe

Projektinformationen
--------------------

.. list-table::
   :widths: 35 65

   * - **Projektname**
     - Smart Window – Intelligente Fenster- und Raumtemperaturüberwachung
   * - **Auftraggeber**
     - Thomas Staub
   * - **Projektleiter**
     - Haiko Nuding
   * - **Projektmitglieder**
     - Haiko Nuding
   * - **Projektausschuss**
     - Haiko Nuding
   * - **Verteiler**
     - Haiko Nuding

Ausgangslage
------------

In meinem Zimmer öffne ich die Fenster regelmässig zum Lüften.
Es kann vorkommen, dass ich am Abend vergesse, sie wieder zu
schliessen. Besonders in der kalten Jahreszeit kann dadurch die
Raumtemperatur sinken und das Zimmer unangenehm kalt werden.

Bisher habe ich keine automatische Überwachung, die mir anzeigt,
welches Fenster offen ist und ob sich mein Zimmer zu stark abkühlt.
Ich möchte daher beide Fenster mit Sensoren ausstatten und die
Raumtemperatur überwachen.

Home Assistant ist bereits installiert und funktionsfähig. Diese
bestehende Installation möchte ich für die Anzeige der Messwerte,
die Konfiguration und die Benachrichtigungen nutzen. Die für das
Projekt benötigte zusätzliche Hardware werde ich selbst kaufen.

Projektziele
------------

Das Ziel ist ein IoT-System, das die Zustände von zwei Fenstern
unabhängig voneinander erkennt, die Raumtemperatur misst und mich
bei Bedarf auf meinem Smartphone benachrichtigt.

Folgende Funktionen sollen im Grundumfang umgesetzt werden:

* **Zwei Fenster überwachen:** Für jedes Fenster wird erkannt,
  ob es offen oder geschlossen ist. Beide Zustände werden
  separat in Home Assistant angezeigt.
* **Raumtemperatur messen:** Ein Temperatursensor erfasst
  regelmässig die Temperatur im Zimmer und übermittelt den
  Messwert an Home Assistant.
* **Individuelle Mindesttemperatur:** In Home Assistant kann
  beispielsweise eine Mindesttemperatur von 22 °C eingestellt
  werden.
* **Abendliche Erinnerung:** Zu einer einstellbaren Uhrzeit,
  beispielsweise 21:00 Uhr, wird geprüft, ob mindestens ein
  Fenster offen ist. Die Benachrichtigung nennt das betroffene
  Fenster beziehungsweise beide Fenster.
* **Temperaturwarnung:** Wenn mindestens ein Fenster offen ist
  und die Raumtemperatur während einer einstellbaren Dauer,
  beispielsweise fünf Minuten, unter der Mindesttemperatur
  liegt, wird eine Warnung gesendet.
* **Dringlichere Warnung:** Bei Unterschreitung einer zweiten,
  tieferen Temperaturgrenze, beispielsweise 19 °C, erfolgt
  eine deutlichere Meldung, sofern ein Fenster offen ist.
* **Benachrichtigungen begrenzen:** Kurze Schwankungen sollen
  keine sofortigen Meldungen auslösen. Wiederholte Meldungen
  sollen begrenzt werden.
* **Dashboard:** Home Assistant zeigt beide Fensterzustände,
  die aktuelle Temperatur und die einstellbaren Grenzwerte.

Die konkreten Temperaturgrenzen und Zeitverzögerungen sind
vorläufige Beispielwerte und werden bei der Umsetzung geprüft.
Eine dringlichere Meldung ist nicht automatisch eine
Smartphone-Systembenachrichtigung, die den Lautlosmodus umgeht.

Optionale Erweiterungen
~~~~~~~~~~~~~~~~~~~~~~~

* Temperaturverlauf als Diagramm darstellen.
* Unterschiedliche Temperaturgrenzen für Tag und Nacht anbieten.
* Erkennen, wenn die Raumtemperatur innerhalb kurzer Zeit
  besonders schnell sinkt.
* Weitere Fenster später ergänzen.

Abgrenzungen
------------

* Die Fenster werden nicht automatisch geöffnet oder geschlossen.
* Die Heizung wird nicht aktiv gesteuert.
* Das Projekt regelt die Raumtemperatur nicht selbstständig,
  sondern dient der Überwachung und Benachrichtigung.
* Es wird nur das Zimmer mit seinen zwei Fenstern überwacht.
* Eine eigene Smartphone-App wird nicht entwickelt;
  vorgesehen ist die Home Assistant Companion App.
* Die optionalen Erweiterungen sind nicht Voraussetzung für
  den erfolgreichen Abschluss des Grundprojekts.

Rahmenbedingungen
-----------------

* Das Projekt wird im Rahmen des IoT-Moduls umgesetzt und in
  Sphinx mit RST-Dateien dokumentiert.
* Home Assistant ist bereits installiert und funktionsfähig.
* Die zusätzliche Hardware wird selbst beschafft und bezahlt.
* Für den Prototyp ist ein ESP32 mit ESPHome vorgesehen.
* Die Sensorwerte werden über das vorhandene WLAN an
  Home Assistant übertragen.
* Der ESP32 soll nach Möglichkeit beide Fensterkontakte und
  den gemeinsamen Raumtemperatursensor auslesen.
* Die Montage soll ohne dauerhafte Beschädigung der Fenster
  möglich sein.
* Die genaue Auswahl der Bauteile sowie die Befestigung
  werden vor dem Kauf geprüft.

Grobkonzept der technischen Lösung
---------------------------------

An jedem der beiden Fenster wird ein magnetischer
Fensterkontakt angebracht. Die Kontakte erkennen unabhängig
voneinander, ob das jeweilige Fenster geöffnet oder geschlossen
ist. Ein Temperatursensor misst die Temperatur im Zimmer.

Ein ESP32 liest die Sensorwerte aus. Über ESPHome und WLAN
werden die Werte in die bereits vorhandene Home-Assistant-
Installation eingebunden. Home Assistant übernimmt die Anzeige,
die einstellbaren Schwellenwerte und die Automatisierungen.

Für den ersten Aufbau ist ein zentraler ESP32 vorgesehen.
Ob die Kabellängen von beiden Fenstern zum ESP32 praktikabel
sind, wird bei der technischen Konzeption überprüft. Bei Bedarf
muss der Aufbau angepasst werden.

Der Temperatursensor soll nicht direkt im kalten Luftzug des
Fensters sitzen, damit er möglichst die Raumtemperatur misst.

Benachrichtigungslogik (geplant)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Beide Fensterkontakte melden ihren aktuellen Zustand.
#. Die Raumtemperatur wird regelmässig erfasst.
#. Zur eingestellten Abendzeit prüft Home Assistant beide
   Fenster. Ist mindestens eines offen, wird eine Erinnerung
   mit Angabe des betroffenen Fensters gesendet.
#. Wenn mindestens ein Fenster offen ist und die Temperatur
   für die eingestellte Verzögerung unter den Mindestwert
   sinkt, wird eine Temperaturwarnung ausgelöst.
#. Wird bei offenem Fenster zusätzlich die kritische
   Temperaturgrenze unterschritten, folgt eine dringlichere
   Benachrichtigung.
#. Sobald beide Fenster geschlossen sind, entfallen die
   fensterabhängigen Warnbedingungen. Neue Warnungen werden
   nur bei erneut erfüllten Bedingungen ausgelöst.

Meilensteine und Termine
------------------------

Die folgenden Abgabetermine stammen aus dem KompetenzHub des
Moduls IoT. Die interne Reihenfolge der Arbeitsschritte wird
an diesen Terminen ausgerichtet.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Datum
     - Lieferobjekt
     - Geplantes Ergebnis
   * - 23.10.2026
     - Projektplanung (09B)
     - Projektidee und grobe Planung
   * - 13.11.2026
     - Initialisierung (09I)
     - Ausgangslage, Ziele, Aufwand, Kosten und Risiken dokumentiert
   * - 04.12.2026
     - Konzept (09I)
     - Hardwareauswahl, Verdrahtung und Automationslogik festgelegt
   * - 18.12.2026
     - Realisierung (09A)
     - Sensoren integriert, Benachrichtigungen getestet und Umsetzung dokumentiert
   * - 15.01.2027
     - Präsentation (10B)
     - Smart-Window-Projekt vorgestellt
   * - 22.01.2027
     - Komplexität (10B)
     - Nachweis zur Projektkomplexität gemäss Modulvorgabe

Geplante interne Arbeitsschritte
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Bis zur Konzeptabgabe: Geeignete Fensterkontakte und einen
  Temperatursensor auswählen, Positionierung und Verkabelung
  planen sowie Bestellmöglichkeiten prüfen.
* Nach Festlegung der Hardware: Komponenten selbst beschaffen,
  beide Fensterkontakte anschliessen und ESPHome konfigurieren.
* Bis zur Realisierungsabgabe: Home-Assistant-Dashboard und
  Benachrichtigungen erstellen, Funktionstests durchführen
  und die Ergebnisse dokumentieren.
* Vor der Präsentation: Projektergebnis, Erfahrungen und
  mögliche Verbesserungen aufbereiten.

Kostenschätzung
--------------

Ich kaufe die benötigte Hardware selbst. Die folgenden Beträge
sind unverbindliche Schätzwerte, keine geprüften Händlerpreise.
Die tatsächlichen Kosten können je nach Modell, Lieferant und
Versandkosten abweichen.

.. list-table::
   :header-rows: 1
   :widths: 50 15 35

   * - Komponente
     - Anzahl
     - Geschätzte Kosten
   * - ESP32-Entwicklungsboard
     - 1
     - CHF 10.00
   * - Magnetische Fensterkontakte
     - 2
     - CHF 10.00
   * - Temperatursensor (z. B. SHT31)
     - 1
     - CHF 10.00
   * - Kabel, Steckverbinder und Befestigung
     - 1 Set
     - CHF 5.00
   * - USB-Netzteil
     - 1
     - CHF 10.00
   * - Versand- und Preisreserve
     - 1
     - CHF 10.00
   * - **Geschätztes Gesamtbudget**
     -
     - **CHF 55.00**

Die bereits funktionierende Home-Assistant-Installation,
der Computer und das Smartphone werden als vorhanden betrachtet
und nicht nochmals budgetiert. Falls bei der Konzeptphase
mehrere Mikrocontroller nötig werden, muss die Kostenschätzung
angepasst werden.

Personenaufwand
---------------

Das Projekt wird von mir alleine umgesetzt. Der Aufwand ist
vorläufig geschätzt und enthält noch keine grössere Reserve
für unerwartete technische Probleme.

.. list-table::
   :header-rows: 1
   :widths: 70 30

   * - Tätigkeit
     - Aufwand
   * - Planung und Initialisierung
     - 2 Stunden
   * - Hardwareauswahl und technisches Konzept
     - 3 Stunden
   * - Beschaffungsvorbereitung und Hardwareaufbau
     - 3 Stunden
   * - ESPHome und Sensoren konfigurieren
     - 3 Stunden
   * - Home Assistant, Dashboard und Automationen
     - 4 Stunden
   * - Funktionstests und Fehlerbehebung
     - 3 Stunden
   * - Dokumentation und Präsentationsvorbereitung
     - 3 Stunden
   * - **Geschätzter Gesamtaufwand**
     - **21 Stunden**

Sachmittel
----------

**Hardware:**

* 1 × ESP32-Entwicklungsboard
* 2 × magnetische Fensterkontakte
* 1 × digitaler Temperatursensor, beispielsweise SHT31
* 1 × geeignetes USB-Netzteil
* Kabel, Steckverbinder und gegebenenfalls Steckbrett
* Material zur Befestigung der Fensterkontakte
* Computer und Smartphone (vorhanden)
* Gerät mit funktionierendem Home Assistant (vorhanden)

**Software:**

* ESPHome
* Home Assistant (bereits eingerichtet)
* Home Assistant Companion App für Smartphone-Benachrichtigungen
* Visual Studio Code
* Sphinx zur Dokumentation
* Git zur Versionsverwaltung

**Hilfsmittel:**

* Schraubendreher und gegebenenfalls Multimeter
* Bei Bedarf Lötkolben für feste Verbindungen

Risikoanalyse
-------------

.. list-table::
   :header-rows: 1
   :widths: 28 17 17 38

   * - Risiko
     - Wahrscheinlichkeit
     - Auswirkung
     - Massnahme
   * - Beide Fenster liegen zu weit vom zentralen ESP32 entfernt
     - Mittel
     - Mittel
     - Kabelführung prüfen; bei Bedarf zweiten ESP32 einplanen
   * - Fensterkontakt erkennt Öffnen oder Schliessen falsch
     - Mittel
     - Hoch
     - Positionierung und Sensorstatus an beiden Fenstern testen
   * - Temperaturmessung wird durch Zugluft verfälscht
     - Mittel
     - Mittel
     - Sensorposition im Raum überprüfen
   * - WLAN oder Home Assistant ist vorübergehend nicht erreichbar
     - Mittel
     - Hoch
     - Verbindungsstatus anzeigen und Ausfälle bei Tests berücksichtigen
   * - Smartphone-Benachrichtigungen werden nicht zugestellt
     - Mittel
     - Hoch
     - Berechtigungen und Companion App mit Testmeldungen prüfen
   * - Zu viele oder doppelte Benachrichtigungen
     - Mittel
     - Mittel
     - Verzögerungen und Wiederholungsregeln definieren
   * - Lieferung verzögert sich
     - Mittel
     - Hoch
     - Bauteile früh bestellen und Alternativen prüfen
   * - Aufwand übersteigt die verfügbare Zeit
     - Mittel
     - Hoch
     - Grundfunktionen priorisieren; Erweiterungen zurückstellen

Erwarteter Nutzen
-----------------

Durch Smart Window werde ich rechtzeitig daran erinnert,
meine Fenster zu schliessen, bevor mein Zimmer unnötig
abkühlt. Beide Fenster können getrennt überwacht werden,
wodurch ich erkennen kann, welches noch offen ist.

Individuell einstellbare Grenzwerte und Erinnerungszeiten
helfen dabei, die Benachrichtigungen an meinen Alltag
anzupassen. Das System heizt nicht selbst, kann aber
unnötige Wärmeverluste durch offen gelassene Fenster
vermeiden helfen.

Mit dem Projekt vertiefe ich meine Kenntnisse über
Sensoren, ESP32, ESPHome, Home Assistant und
IoT-Automatisierungen sowie über Planung, Test und
Dokumentation eines technischen Projekts.

Projektfreigabe
--------------

Dieser Initialisierungsbericht dient als Grundlage für
die Abstimmung des Projektumfangs mit dem Auftraggeber
Thomas Staub. Nach der Freigabe wird das technische
Konzept ausgearbeitet und anschliessend die Realisierung
umgesetzt.

**Freigabestatus:** Ausstehend
