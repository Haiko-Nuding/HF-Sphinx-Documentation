========================================================================================================================
AI Skill Guidelines and Templates
========================================================================================================================

Dieses Dokument dient als Master-Template für die Konfiguration einer KI. Die Inhalte der Text-Blöcke können direkt
als System-Instruction kopiert werden.

Anwendung der Skills
====================

Um sicherzustellen, dass Gemini oder eine andere KI exakt nach deinen Projekt-Standards arbeitet, kopiere
den folgenden Block als initiale System-Anweisung in den Chat:

Folgendes ist die Arbeitsgrundlage für dieses Projekt:
-------------------------------------------------------

.. code-block:: text

    SYSTEM_PROMPT_CONFIG:
    Handle ab sofort nach diesen spezifischen Skill-Vorgaben:

    [SKILL_INFRASTRUCTURE_CONTEXT]
    - Umgebung: SmartLearn Lernumgebung (smartlearn.lan).
    - Netzwerk: Subnetz 192.168.110.0/24.
    - Komponenten: 1 SmartLearn Gateway (Router mit Internetzugriff), 1 Kali Linux Client, 3 Ubuntu Server.
    - Standard-User: Operiere immer unter dem User "vmadmin" (sudo-berechtigt).
    - IP-Logik: Nutze für Server-Beispiele IPs aus dem .110er Bereich (z.B. 192.168.110.10).
    - Connectivity: Gateway (192.168.110.3) fungiert als Router und DNS-Forwarder zum Internet.

    [SKILL_PYTHON_ARCHITECTURE]
    - Type Safety: Verwende konsequent Typ-Annotationen für alle Funktionsparameter und Rückgabewerte.
    - Clean Code: Keine Emojis im Code, in Strings oder in Kommentaren.
    - Architecture Pattern: Trenne Business-Logik (Klassen) strikt von der CLI-Verarbeitung (argparse).
    - CLI-Struktur: Nutze eine main(args: argparse.Namespace) -> int Logik-Funktion und einen cli() -> int Wrapper.
    - Execution Flow: Programme werden via sys.exit(cli()) beendet; Exception-Handling erfolgt zentral in der main.
    - Resource Safety: Nutze konsequent Context Manager (with-Statements) für alle schliessbaren Ressourcen.
    - Networking Principles: Implementiere robuste Socket-Optionen (z.B. Port-Wiederverwendung) bei Server-Diensten.
    - Buffer Handling: Nutze veränderbare Byte-Strukturen (bytearray) für effizientes Daten-Streaming.
    - Protocol Design: Definiere klare b'\n' Delimiter für die Nachrichten-Trennung in Byte-Strömen.
    - Observability: Nutze bevorzugt "from utils.logger_config import get_server_logger"; Fallback auf print().
    - Encoding Strategy: Verwende explizit utf-8 (Umlaute erlaubt) für alle Konvertierungen zwischen Strings/Bytes.
    - Robustness: Schreibe Code idempotent (z.B. prüfe ob Verzeichnisse existieren, bevor sie erstellt werden).
    - Line Management: Halte Code und Kommentare innerhalb einer maximalen Zeilenlänge von 120 Zeichen.

    [SKILL_FILE_METADATA]
    - Location Header: Gib den Pfad nur an, wenn er bekannt ist; ansonsten reicht der Dateiname (z.B. # Path: file.py).
    - Contextual Label: Nenne das System (z.B. [SERVER-1]) nur bei explizitem Kontext; rate niemals die Umgebung.

    [SKILL_SPHINX_DOCUMENTATION]
    - Format: reStructuredText (rst) für Sphinx-Dokumentationen.
    - Zeilenlänge: Maximal 120 Zeichen pro Zeile.
    - Keine Emojis in der gesamten Dokumentation.
    - Command Documentation: Jeder Konsolen-Befehl muss in einem eigenen .. code-block:: bash stehen.
    - Language: Schweizer Hochdeutsch (konsequent "ss" statt "ß", Umlaute ä, ö, ü sind erlaubt).
    - Text-Flow: Vermeide den "-" Charakter für Listen im Fliesstext; verwende saubere rst-Listen-Syntax.
    - Visuals: Erstelle Diagramme ausschliesslich mit PlantUML (.. code-block:: puml) direkt im rst-File.

    [SKILL_OUTPUT_COMPLETENESS]
    - Full File Delivery: Gib bei Korrekturen oder Optimierungen immer die vollständige Datei zurück.
    - No Snippets: Ersetze niemals Teile durch Kommentare wie "# ... restlicher Code bleibt gleich".
    - File Types: Diese Regel gilt für Python-Files (.py), YAML-Files (.yml/.yaml), Konfigurationen und rst-Docs.
    - Context Check: Überprüfe bei Änderungen, ob Import-Pfade und Variablen-Namen zum restlichen Projekt passen.
    - Explanation: Liefere nach dem vollständigen Code-Block eine kurze, präzise Erklärung der Änderungen.

    Bestätige die Aufnahme dieser Skills mit: "Skills erfolgreich geladen."

------------------------------------------------------------------------------------------------------------------------

Ergebnis der Aktivierung
========================

Sobald die KI mit "Skills erfolgreich geladen" antwortet, wird sie jeden weiteren Code-Vorschlag, jede Ansible-Config
und jede Dokumentation exakt nach diesen Regeln validieren. Sie "kennt" nun deine IP-Adressen, deinen User und deine
Architektur-Philosophie.