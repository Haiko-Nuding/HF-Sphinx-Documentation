==========================================
Fokus-Modul: Social Engineering
==========================================

.. meta::
   :description: Kompaktwissen zu Social Engineering Techniken und Mustern.

Definition & Kernkonzept
-------------------------

Social Engineering ist kein technischer Hack, sondern die **gezielte Manipulation von Menschen**. Das Ziel ist es, Personen dazu zu bringen, freiwillig Handlungen auszuführen, die ihre Sicherheit oder die der Organisation gefährden.

.. admonition:: Was es NICHT ist

   * **Keine Software-Exploits:** Es werden keine Programmierfehler ausgenutzt.
   * **Kein Technikeinbruch:** Firewalls und MFA bleiben technisch intakt, werden aber durch den Faktor "Mensch" umgangen.



Die 5 Muster des Angriffs
-------------------------

Ein Angreifer ist meist dann erfolgreich, wenn mindestens **drei** dieser psychologischen Faktoren zusammenspielen:

1. **Vertrauen:** Aufbau einer (vorgetäuschten) Beziehung.
2. **Glaubwürdigkeit:** Erzeugen eines plausiblen Kontextes (z.B. IT-Support).
3. **Handlungsaufforderung:** Ein konkreter Klick oder eine Dateneingabe.
4. **Zeitdruck:** Stress erzeugen, um kritisches Denken auszuschalten.
5. **Konsequenz:** Androhen von negativen Folgen (z.B. Kontosperrung).

Angriffsformen im Vergleich
---------------------------

Hier sind die gängigsten Techniken kurz und prägnant gegenübergestellt:

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Technik
     - Beschreibung
     - Motivator
   * - **Phishing**
     - Massen-Mails mit Fake-Links oder Anhängen.
     - Angst / Routine
   * - **Spear Phishing**
     - Hochgradig personalisierte Angriffe auf Einzelpersonen.
     - Vertrauen
   * - **Baiting**
     - Präparierte USB-Sticks oder Downloads („Lohnliste“).
     - Neugier / Gier
   * - **Pretexting**
     - Vorspielen einer falschen Identität (HR, Behörde).
     - Autorität
   * - **Scareware**
     - Falsche Warnmeldungen über Infektionen.
     - Angst / Panik
   * - **Pharming**
     - Manipulation von DNS, um User auf Fake-Seiten zu leiten.
     - Täuschung



Spezialfall: Business Email Compromise (CEO-Fraud)
--------------------------------------------------

Diese Methode verzichtet oft komplett auf Malware oder Links. Der Angreifer nutzt lediglich **legitime Geschäftsprozesse** und die **Autorität** der Geschäftsleitung aus, um dringende Überweisungen zu veranlassen.

.. tip::

   Hier scheitern technische Schutzmassnahmen wie Firewalls komplett, da die Kommunikation oft über echte (aber kompromittierte) oder täuschend echte Mail-Accounts läuft.


Interaktive Checkfragen
-----------------------

.. admonition:: Analyse-Training
   :class: note

   Stellen Sie sich vor, Sie erhalten eine sprachlich perfekte Mail vom "IT-Dienstleister" mit Bezug auf ein aktuelles Projekt und der Bitte, kurz ein Passwort zu bestätigen.

   * Welche **Muster** werden hier bedient?
   * Warum greifen hier **MFA-Lösungen** oft zu kurz?
   * Wie würde ein aufmerksamer Nutzer den Angriff entlarven?