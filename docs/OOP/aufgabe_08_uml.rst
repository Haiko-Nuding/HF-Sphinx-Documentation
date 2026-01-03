Aufgabe 08 UML
==============

Eigenes Fallbeispiel (Online-Essen)
-----------------------------------

Dieses Modul behandelt ein eigenes Fallbeispiel: Ein **Online-Essen-Bestellsystem**, welches Kunden, Warenkörbe, Produkte und Lieferungen verwaltet.

Klassendiagramm
---------------

Hier ist die visuelle Darstellung der Klassenstruktur für das Bestellsystem:

.. plantuml::

   @startuml
   skinparam classAttributeIconSize 0

   package OnlineEssenSystem {

       class Produkt {
           + Name : string
           + Preis : double
           + Produkt(name : string, preis : double)
       }

       class Warenkorb {
           + Artikel : List<Produkt>
           + Gesamtpreis : double
           + ArtikelHinzufuegen(p : Produkt) : void
       }

       class Kunde {
           + Name : string
           + Adresse : string
           + AktuellerWarenkorb : Warenkorb
           + Kunde(name : string, adresse : string)
       }

       class Lieferung {
           + LieferID : int
           + Status : string
           + ZielKunde : Kunde
           + Lieferung(id : int, kunde : Kunde)
       }

       Kunde "1" *-- "1" Warenkorb : besitzt
       Warenkorb "1" o-- "*" Produkt : enthält
       Lieferung "1" --> "1" Kunde : wird geliefert an
   }
   @enduml



Klassenbeschreibung
-------------------

Produkt
    Repräsentiert eine Speise oder ein Getränk mit einem Namen und einem Preis.

Warenkorb
    Dient als Sammelstelle für ausgewählte Produkte und berechnet automatisch den Gesamtpreis der enthaltenen Artikel.

Kunde
    Enthält die Stammdaten des Bestellers, wie Name und Lieferadresse, und ist fest mit einem Warenkorb verknüpft.

Lieferung
    Verknüpft eine Bestellung mit einem Kunden und dokumentiert den aktuellen Fortschritt (Status) der Zustellung.

Wichtige Logik
--------------

* **Automatisierung:** Der Warenkorb berechnet bei jedem hinzugefügten Produkt den Gesamtpreis neu.
* **Status-Tracking:** Die Lieferung ermöglicht es, den Status von "In Vorbereitung" auf "Unterwegs" oder "Geliefert" zu setzen.
* **Instanziierung:** Im Programmcode werden für jeden Typ mindestens zwei Instanzen erstellt, um den Datenfluss zwischen Kunden und Lieferdienst zu simulieren.
