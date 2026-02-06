Aufgabe 05 UML
==============

Dieses Modul behandelt die Verwaltung eines Zoos mit Gehegen, Tieren und Pflegern.

Klassendiagramm
---------------

Hier ist die visuelle Darstellung der Klassenstruktur:

.. plantuml::

   @startuml
   skinparam classAttributeIconSize 0

   package Aufgabe_05 {
       class Art {
           + Name : string
           + Art()
           + Art(name : string)
       }

       class Tier {
           + Name : string
           + Alter : int
           + Art : Art
           + Tier()
           + Tier(name : string, alter : int, art : Art)
       }

       class Pfleger {
           + Name : string
           + Adresse : string
           + Notallnummer : string
           + Pfleger()
           + Pfleger(name : string, adresse : string, notfallnummer : string)
       }

       class Gehege {
           - _maximaleAnzahlTiere : int
           + Groesse : string
           + MaximaleAnzahlTiere : int
           + Baujahr : int
           - TiereListe : List<Tier>
           - PflegerListe : List<Pfleger>
           + AnzahlTiere : int
           + Gehege()
           + Gehege(groesse : string, maximaleAnzahlTiere : int, baujahr : int)
           + TierHinzufuegen(neuesTier : Tier) : bool
           + TierLoeschen(tier : Tier) : void
           + PflegerHinzufuegen(pfleger : Pfleger) : void
           + PflegerLöschen(pfleger : Pfleger) : void
           + Info() : void
       }

       class Futterung {
           + Gewicht : double
           + Nahrungsmittel : string
           + Gehege : Gehege
           + Erstellungsdatum : DateTime
           + Futterung()
           + Futterung(nahrungsmittel : string, gewicht : double)
           + IstAelterAls3Jahre() : bool
       }

       Tier "1" --> "1" Art : gehört zu
       Gehege "1" o-- "*" Tier : enthält
       Gehege "1" o-- "*" Pfleger : betreut von
       Futterung "1" --> "1" Gehege : findet statt in
   }
   @enduml

Klassenbeschreibung
-------------------

Tier
    Repräsentiert ein einzelnes Tier im Zoo. Es ist einer bestimmten **Art** zugeordnet.

Gehege
    Verwaltet eine Liste von Tieren und Pflegern. Es gibt eine Kapazitätsgrenze für die Anzahl der Tiere.

Pfleger
    Enthält Kontaktinformationen der Mitarbeiter, die für die Gehege zuständig sind.

Fütterung
    Dokumentiert die Verpflegung der Tiere in einem bestimmten Gehege.

Wichtige Logik
--------------

* **Validierung:** Das Gehege prüft beim Hinzufügen eines Tieres, ob noch Platz frei ist.
* **Datum:** Die Fütterung speichert automatisch das aktuelle Erstellungsdatum.
* **Bereinigung:** Fütterungsdaten, die älter als 3 Jahre sind, können identifiziert werden.
