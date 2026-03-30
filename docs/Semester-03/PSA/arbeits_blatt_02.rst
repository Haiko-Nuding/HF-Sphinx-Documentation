=======================================
Netzwerk-Grundlagen & Protocol Analysis
=======================================

Einleitung
----------
In dieser Woche untersuchen wir die Anatomie einer Netzwerkverbindung. Wir wechseln von der reinen Theorie zur praktischen Analyse mittels Sockets und Wireshark.

Der TCP Handshake (PlantUML)
----------------------------
Bevor Daten fließen können, müssen Client und Server eine stabile Verbindung aushandeln. Dies geschieht über den **Three-Way-Handshake**.

.. only:: html

    .. uml::

       @startuml
       participant Client
       participant Server

       Client -> Server: SYN (Synchronize)
       Note right: "Ich möchte eine Verbindung auf Port 6543"
       Server -> Client: SYN-ACK (Synchronize-Acknowledge)
       Note left: "Ich habe Zeit und bin bereit"
       Client -> Server: ACK (Acknowledge)
       Note right: "Alles klar, Verbindung steht!"

       Client -> Server: PSH, ACK (Payload/Daten)
       Note right: Hier wird das JSON-Paket gesendet
       Server -> Client: ACK (Bestätigung Erhalt)
       @enduml

Wireshark Analyse: Der Blick ins Kabel
--------------------------------------

Warum das "Loopback" Interface?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Wenn wir ``127.0.0.1`` (Localhost) verwenden, verlassen die Datenpakete unseren Computer nie. Sie werden nicht an die physische Netzwerkkarte (Ethernet/WLAN) gesendet, sondern intern "kurzgeschlossen".

* **Standard-Interfaces (eth0/wlan0):** Überwachen den echten Netzwerkverkehr nach außen.
* **Loopback (lo):** Ist ein virtuelles Interface, das nur den internen Verkehr des eigenen Rechners sieht. Da unser Client und Server auf derselben Maschine laufen, ist Wireshark auf ``lo`` zwingend erforderlich.



Die Bedeutung von [PSH, ACK]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In Wireshark sehen wir verschiedene "Flags". Das Flag **[PSH] (Push)** ist für uns das wichtigste:

1. **Kontroll-Pakete:** SYN, ACK oder FIN sind meist leer und dienen nur dem Management der Verbindung.
2. **Daten-Pakete:** Wenn das [PSH]-Flag gesetzt ist, signalisiert der Sender dem Empfänger: *"Ich schicke dir jetzt echte Daten (Payload), verarbeite sie sofort!"*
3. In der Liste erkennen wir diese Pakete oft an der höheren **Length** (z.B. 367 Bytes statt 66 Bytes).

Payload finden und extrahieren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Um die unverschlüsselte Nachricht (Confidentiality-Verletzung) zu beweisen, gehen wir wie folgt vor:

1. **Paket auswählen:** Das Paket mit dem ``[PSH, ACK]`` Flag anklicken.
2. **Daten-Bereich:** Im unteren Fenster die Schicht **"Data"** oder **"Transmission Control Protocol"** aufklappen.
3. **Kopieren:**
   * Rechtsklick auf den Hex-Bereich (unten rechts).
   * **Copy -> ...as a Hex Dump:** Um den digitalen Fingerabdruck zu zeigen.
   * **Copy -> ...as Printable Text:** Um den lesbaren Inhalt (JSON) zu erhalten.

Beweis: Der unverschlüsselte JSON-Inhalt
----------------------------------------
Wie im Wireshark-Log ersichtlich, wird das gesamte JSON-Objekt im Klartext übertragen. Ein Angreifer kann alle Felder (Sender, Content, Timestamp) ohne Schlüssel mitlesen.

**Extrahiertes JSON-Beispiel:**

.. code-block:: json

   {
     "sender": "Client Nr. 12421",
     "content": "Wir senden Nachricht 1 Bloat [0, 1, 2, ...]",
     "timestamp": "31.03.2026 01:33:10"
   }

Fazit Woche 2
-------------
Wir haben erfolgreich eine Kommunikation etabliert, aber die **CIA-Triade** ist unvollständig. Die Vertraulichkeit (Confidentiality) fehlt komplett. Dies ist der Startpunkt für Woche 3: Die Implementierung von **Symmetrischer Verschlüsselung**.