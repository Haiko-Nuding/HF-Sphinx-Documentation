========================================================================================================================
PSA Python Module Tutorial: Key Modules & Code Examples
========================================================================================================================

Dieses Dokument beschreibt die Kern-Module des Projekts mit Fokus auf deren praktische Anwendung.

1. Cryptography (Fernet) - Third-Party
======================================

Das Modul ``cryptography`` stellt mit ``Fernet`` eine sichere, symmetrische Verschlüsselung bereit.

**Typische Verwendung:**

.. code-block:: python

    from cryptography.fernet import Fernet

    # 1. Schlüssel erstellen und laden
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # 2. Daten verschlüsseln (muss vom Typ 'bytes' sein)
    message = "Geheimdaten 123".encode('utf-8')
    cipher_text = cipher_suite.encrypt(message)

    # 3. Daten entschlüsseln
    plain_text = cipher_suite.decrypt(cipher_text).decode('utf-8')
    print(f"Original: {plain_text}")

*Im Projekt:* Sichert die JSON-Pakete vor dem Versenden über das Netzwerk ab.

------------------------------------------------------------------------------------------------------------------------

2. Asyncio - Standard Library
=============================

Ermöglicht asynchrone Programmierung, um I/O-Wartezeiten (wie Netzwerk-Timeouts) zu überbrücken.

**Typische Verwendung:**

.. code-block:: python

    import asyncio

    async def check_service(name, delay):
        await asyncio.sleep(delay)
        print(f"Service {name} ist bereit.")

    async def main():
        # Startet mehrere Aufgaben gleichzeitig
        await asyncio.gather(
            check_service("Scanner", 1),
            check_service("Logger", 0.5)
        )

    asyncio.run(main())

*Im Projekt:* Erlaubt dem ``AsyncPortScanner`` hunderte Ports gleichzeitig zu prüfen, statt nacheinander zu warten.



------------------------------------------------------------------------------------------------------------------------

3. Socket - Standard Library
============================

Die Basis für jegliche Netzwerkkommunikation über TCP/IP.

**Typische Verwendung (Client-Seite):**

.. code-block:: python

    import socket

    # Verbindung aufbauen (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 6543))
        s.sendall(b"Hallo Server")
        data = s.recv(1024)
        print(f"Empfangen: {data.decode()}")

*Im Projekt:* Bildet die "Leitung", durch die unsere verschlüsselten JSON-Daten fließen.

------------------------------------------------------------------------------------------------------------------------

4. Argparse - Standard Library
==============================

Modul zum Erstellen von professionellen Kommandozeilen-Schnittstellen (CLI).

**Typische Verwendung:**

.. code-block:: python

    import argparse

    parser = argparse.ArgumentParser(description="Tool Beschreibung")
    parser.add_argument("--ip", default="127.0.0.1", help="Ziel-IP Adresse")
    parser.add_argument("--port", type=int, required=True, help="Ziel-Port")

    args = parser.parse_args()
    print(f"Verbinde zu {args.ip} auf Port {args.port}")

*Im Projekt:* Ermöglicht die Steuerung von Host, Port und Verschlüsselungs-Modus beim Starten der Skripte.

------------------------------------------------------------------------------------------------------------------------

Modul-Klassifizierung
=====================

.. list-table:: Übersicht der Abhängigkeiten
   :widths: 25 25 50
   :header-rows: 1

   * - Modul
     - Typ
     - Installationspfad (Linux/Venv)
   * - cryptography
     - Third-Party
     - ``.venv/lib/python3.x/site-packages/``
   * - asyncio
     - Standard
     - ``/usr/lib/python3.x/asyncio/``
   * - socket
     - Standard
     - Build-in (C-Erweiterung/Standard Lib)
   * - argparse
     - Standard
     - ``/usr/lib/python3.x/argparse.py``