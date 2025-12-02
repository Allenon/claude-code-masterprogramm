# filesystem_agent.py - AUSFÜHRLICH DOKUMENTIERT
"""
FileSystem Agent: Autonome Code-Analyse

ZWECK:
Dieser Agent demonstriert, wie ein AI-Agent vollständig autonom
ein Verzeichnis analysieren kann, indem er:
1. Tools eigenständig nutzt (bash, read_file)
2. Entscheidungen während der Ausführung trifft
3. Mehrere Iterationen durchläuft
4. Einen strukturierten Report erstellt

ARCHITEKTUR:
┌─────────────────┐
│  FileSystemAgent│  ← Main Class
└────────┬────────┘
         │
    ┌────┴────┐
    │ Tools   │  ← bash, read_file
    └────┬────┘
         │
    ┌────┴────┐
    │Agent Loop│ ← Iterativer Prozess
    └─────────┘
"""

# ============================================================================
# IMPORTS
# ============================================================================
import anthropic  # Anthropic Claude API Client
import os         # Für Dateisystem-Operationen und Umgebungsvariablen
from dotenv import load_dotenv  # Lädt .env Datei für API Key

# Lade Umgebungsvariablen aus .env Datei
# Dies macht ANTHROPIC_API_KEY verfügbar via os.getenv()
load_dotenv()


# ============================================================================
# FILESYSTEM AGENT CLASS
# ============================================================================
class FileSystemAgent:
    """
    Der FileSystem Agent ist eine Klasse, die einen autonomen AI-Agent kapselt.
    
    KONZEPT:
    - Der Agent hat Zugriff auf Tools (bash, read_file)
    - Der Agent entscheidet selbst, wann er welches Tool nutzt
    - Der Agent arbeitet in einem Loop bis die Aufgabe erledigt ist
    
    WARUM EINE KLASSE?
    - Kapselt State (client, tools)
    - Wiederverwendbar
    - Saubere Trennung von Concerns
    """
    
    def __init__(self):
        """
        Initialisierung des Agents
        
        HIER PASSIERT:
        1. Anthropic Client wird erstellt (für API-Zugriff)
        2. Tools werden definiert (Agent's "Fähigkeiten")
        """
        
        # ----------------------------------------------------------------
        # SCHRITT 1: Anthropic Client initialisieren
        # ----------------------------------------------------------------
        # Der Client ist unsere Verbindung zur Claude API
        # api_key wird aus .env geladen via os.getenv()
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # ----------------------------------------------------------------
        # SCHRITT 2: Tools definieren
        # ----------------------------------------------------------------
        # Tools sind "Funktionen", die der Agent aufrufen kann
        # Jedes Tool hat:
        # - name: Identifier
        # - description: Was kann das Tool?
        # - input_schema: Welche Parameter braucht es?
        
        self.tools = [
            # TOOL 1: BASH
            # Ermöglicht dem Agent, bash commands auszuführen
            {
                "name": "bash",
                "description": "Execute bash commands to interact with file system",
                
                # input_schema definiert die Parameter nach JSON Schema Standard
                "input_schema": {
                    "type": "object",  # Tool erwartet ein Objekt
                    "properties": {
                        "command": {
                            "type": "string",  # Parameter ist ein String
                            "description": "The bash command to execute"
                        }
                    },
                    "required": ["command"]  # "command" ist Pflichtfeld
                }
            },
            
            # TOOL 2: READ_FILE
            # Ermöglicht dem Agent, Dateien zu lesen
            {
                "name": "read_file",
                "description": "Read the complete content of a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["filepath"]
                }
            }
        ]
        
        # WICHTIG: Die Tools sind nur DEFINITIONEN
        # Die tatsächliche Implementierung ist in bash_tool() und read_file_tool()
    
    
    # ========================================================================
    # TOOL IMPLEMENTATIONS
    # ========================================================================
    
    def bash_tool(self, command: str) -> str:
        """
        Führt einen bash command aus und gibt das Ergebnis zurück
        
        WARUM SUBPROCESS?
        - subprocess.run() ist die sichere Methode, externe Commands auszuführen
        - Alternative wäre os.system() - aber weniger Kontrolle
        
        PARAMETER:
        - command: Der bash command als String
        
        RETURN:
        - stdout (normale Ausgabe) oder stderr (Fehler-Ausgabe)
        """
        import subprocess  # Für sichere Command-Ausführung
        
        try:
            # subprocess.run() führt den Command aus
            result = subprocess.run(
                command,              # Der Command
                shell=True,           # Nutze Shell (erlaubt pipes, redirects, etc.)
                capture_output=True,  # Fange stdout und stderr ein
                text=True,            # Gib Ausgabe als String zurück (nicht bytes)
                timeout=10,           # Max 10 Sekunden (verhindert hanging)
                cwd=os.path.dirname(os.path.abspath(__file__))  # Working Directory
            )
            
            # ENTSCHEIDUNG: stdout oder stderr zurückgeben
            # stdout = normale Ausgabe (z.B. Dateiliste)
            # stderr = Fehler oder Warnings
            output = result.stdout if result.stdout else result.stderr
            
            # Falls keine Ausgabe, gib Erfolgsmeldung zurück
            return output if output else "Command executed successfully (no output)"
            
        except Exception as e:
            # Bei Fehler (z.B. timeout), gib Fehlermeldung zurück
            return f"Error: {str(e)}"
    
    
    def read_file_tool(self, filepath: str) -> str:
        """
        Liest eine Datei und gibt den Inhalt zurück
        
        WARUM ENCODING='UTF-8'?
        - Python Files sind fast immer UTF-8
        - Verhindert Encoding-Fehler bei Umlauten, etc.
        
        FEHLERBEHANDLUNG:
        - try/except fängt alle Fehler (Datei existiert nicht, keine Permission, etc.)
        """
        try:
            # PFAD-HANDLING: Relative Pfade absolut machen
            # Warum? Agent könnte relative Pfade übergeben (z.B. "../test-data/example1.py")
            if not os.path.isabs(filepath):
                # Finde das Verzeichnis, in dem dieses Script liegt
                base_dir = os.path.dirname(os.path.abspath(__file__))
                # Kombiniere mit relativem Pfad
                filepath = os.path.join(base_dir, filepath)
            
            # Öffne und lese Datei
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            # Bei Fehler, gib informative Fehlermeldung zurück
            return f"Error reading file: {str(e)}"
    
    
    # ========================================================================
    # AGENT LOOP - DAS HERZSTÜCK
    # ========================================================================
    
    def analyze_directory(self, directory: str) -> str:
        """
        Die Hauptfunktion: Analysiert ein Verzeichnis vollständig autonom
        
        AGENT LOOP KONZEPT:
        1. Gib dem Agent eine Aufgabe (task)
        2. Agent plant nächsten Schritt
        3. Agent nutzt Tools
        4. Agent bekommt Ergebnis
        5. Agent passt Plan an
        6. Wiederhole bis fertig
        
        Das ist der Unterschied zu traditionellem Code:
        - Traditionell: WIR definieren jeden Schritt
        - Agentic: AGENT entscheidet jeden Schritt
        """
        
        # ----------------------------------------------------------------
        # SCHRITT 1: Task Definition
        # ----------------------------------------------------------------
        # Der Task ist die "Anweisung" an den Agent
        # WICHTIG: Wir sagen WAS, nicht WIE!
        task = f"""
Analysiere das Verzeichnis: {directory}

Aufgaben:
1. Finde alle Python-Dateien (.py) in diesem Verzeichnis
2. Für jede Datei:
   - Lies den Inhalt
   - Zähle Lines of Code (ohne leere Zeilen und Kommentare)
   - Extrahiere alle import-Statements
   - Finde alle TODO und FIXME Kommentare mit Zeilennummer
3. Erstelle einen strukturierten Markdown-Report mit:
   - Übersicht (Anzahl Files, Total LOC)
   - Details pro Datei
   - Liste aller gefundenen TODOs/FIXMEs
   - Liste aller verwendeten Dependencies

Nutze die verfügbaren Tools autonom und systematisch.
Arbeite Datei für Datei durch.
"""
        
        # ----------------------------------------------------------------
        # SCHRITT 2: Messages Array initialisieren
        # ----------------------------------------------------------------
        # Die API erwartet ein Array von Messages
        # Format: [{"role": "user"/"assistant", "content": "..."}]
        # Dies ermöglicht Multi-Turn Conversations
        messages = [{"role": "user", "content": task}]
        
        # User Feedback
        print("🤖 FileSystem Agent gestartet...")
        print(f"📁 Analysiere: {directory}\n")
        
        # ----------------------------------------------------------------
        # SCHRITT 3: Agent Loop Setup
        # ----------------------------------------------------------------
        iteration = 0  # Zähler für Iterationen
        max_iterations = 25  # Sicherheits-Limit (verhindert infinite loops)
        
        # ----------------------------------------------------------------
        # SCHRITT 4: DER AGENT LOOP
        # ----------------------------------------------------------------
        # Dies ist das Herzstück: Der Agent arbeitet iterativ
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Iteration {iteration}")
            
            # ============================================================
            # API CALL: Sende Messages an Claude
            # ============================================================
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # Das Claude Model
                max_tokens=4096,                    # Max Output-Länge
                tools=self.tools,                   # Verfügbare Tools
                messages=messages                   # Conversation History
            )
            
            # WICHTIG: response.stop_reason sagt uns, WARUM Claude gestoppt hat
            # Mögliche Werte:
            # - "end_turn": Agent ist fertig, hat finale Antwort
            # - "tool_use": Agent möchte Tool nutzen
            # - "max_tokens": Output zu lang (sollte nicht passieren bei 4096)
            
            # ============================================================
            # FALL 1: Agent ist FERTIG
            # ============================================================
            if response.stop_reason == "end_turn":
                # Agent hat entschieden: Aufgabe erledigt!
                # response.content ist ein Array von Content-Blocks
                # Wir suchen den Text-Block
                
                final_text = next(
                    # Generator Expression: Finde ersten Block mit .text Attribut
                    (block.text for block in response.content if hasattr(block, "text")),
                    None  # Default falls nichts gefunden
                )
                
                if final_text:
                    print("\n✅ Agent fertig!\n")
                    return final_text
                else:
                    return "Agent finished but no text output found"
            
            # ============================================================
            # FALL 2: Agent möchte TOOL NUTZEN
            # ============================================================
            elif response.stop_reason == "tool_use":
                # Agent hat entschieden: Ich brauche ein Tool!
                
                # Schritt 1: Füge Agent's Response zu Messages hinzu
                # WARUM? API braucht komplette Conversation History
                messages.append({
                    "role": "assistant",
                    "content": response.content  # Enthält tool_use blocks
                })
                
                # Schritt 2: Führe alle Tool-Calls aus
                tool_results = []  # Sammle alle Ergebnisse
                
                # Iteriere über alle Content-Blocks
                for block in response.content:
                    # Prüfe ob es ein tool_use block ist
                    if block.type == "tool_use":
                        tool_name = block.name
                        print(f"  🔧 Tool: {tool_name}", end="")
                        
                        # Führe das entsprechende Tool aus
                        if tool_name == "bash":
                            # block.input ist ein dict mit den Parametern
                            cmd = block.input['command']
                            print(f" → {cmd}")
                            # Führe unser bash_tool aus
                            result = self.bash_tool(cmd)
                            
                        elif tool_name == "read_file":
                            filepath = block.input['filepath']
                            print(f" → {filepath}")
                            # Führe unser read_file_tool aus
                            result = self.read_file_tool(filepath)
                            
                        else:
                            # Unbekanntes Tool (sollte nicht passieren)
                            result = f"Unknown tool: {tool_name}"
                        
                        # Erstelle tool_result für API
                        # Format wird von Anthropic API vorgegeben
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,  # Verknüpfung zum tool_use
                            "content": result         # Das Ergebnis als String
                        })
                
                # Schritt 3: Füge Tool-Ergebnisse zu Messages hinzu
                # Der Agent bekommt nun die Ergebnisse und kann weitermachen
                messages.append({
                    "role": "user",        # Tool-Results kommen als "user"
                    "content": tool_results
                })
                
                # Loop geht weiter - Agent bekommt Chance zu reagieren
            
            # ============================================================
            # FALL 3: Unerwarteter Stop Reason
            # ============================================================
            else:
                print(f"⚠️ Unexpected stop reason: {response.stop_reason}")
                break
        
        # Falls max_iterations erreicht
        return "❌ Max iterations reached without completion"


# ============================================================================
# MAIN FUNCTION - ENTRY POINT
# ============================================================================
def main():
    """
    Main Function: Startet den Agent und gibt Report aus
    
    ABLAUF:
    1. Agent instanzieren
    2. Aufgabe geben (analyze_directory)
    3. Report ausgeben
    4. Report speichern
    """
    
    # Erstelle Agent-Instanz
    agent = FileSystemAgent()
    
    # Definiere Ziel-Verzeichnis
    # "../test-data" ist relativ zum aktuellen Script
    test_dir = "../test-data"
    
    # User Interface: Header
    print("=" * 70)
    print("🔍 FILESYSTEM AGENT - Autonome Code-Analyse")
    print("=" * 70)
    print("\n")
    
    # HIER PASSIERT DIE MAGIE: Agent arbeitet vollständig autonom
    report = agent.analyze_directory(test_dir)
    
    # Zeige Report
    print("\n" + "=" * 70)
    print("📊 ANALYSIS REPORT")
    print("=" * 70)
    print("\n")
    print(report)
    
    # Speichere Report als Markdown-Datei
    output_file = "analysis_report.md"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(report)
    
    # Erfolgs-Message
    print("\n" + "=" * 70)
    print(f"✅ Report gespeichert: {output_file}")
    print("=" * 70)


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
# Dieser Block wird nur ausgeführt, wenn das Script direkt gestartet wird
# (nicht wenn es importiert wird)
if __name__ == "__main__":
    main()


# ============================================================================
# ZUSAMMENFASSUNG: WIE FUNKTIONIERT DER AGENT LOOP?
# ============================================================================
"""
SCHRITT-FÜR-SCHRITT:

1. USER gibt Task
   └─> messages = [{"role": "user", "content": "Analysiere ..."}]

2. AGENT überlegt und antwortet
   └─> API Call mit messages + tools
   └─> response.stop_reason = "tool_use"
   └─> response.content = [tool_use block]

3. WIR führen Tool aus
   └─> bash_tool("find ...") oder read_file_tool("example1.py")
   └─> result = "example1.py\nexample2.py\n..."

4. WIR geben Result zurück an Agent
   └─> messages.append({"role": "user", "content": [tool_result]})

5. AGENT bekommt Result und überlegt weiter
   └─> Nächster API Call mit erweiterten messages
   └─> Entweder: tool_use (braucht noch Tool) oder end_turn (fertig!)

6. WIEDERHOLEN bis Agent sagt "end_turn"
   └─> Agent gibt finalen Report zurück

WICHTIGE ERKENNTNISSE:

❌ Traditioneller Code:
   Wir: "Mach Schritt 1, dann 2, dann 3"
   
✅ Agentic Code:
   Wir: "Hier ist das Ziel. Du hast diese Tools. Go!"
   Agent: Entscheidet selbst jeden Schritt

Das ist ECHTE Autonomie! 🚀
"""