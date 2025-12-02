# filesystem_agent.py
"""
FileSystem Agent: Autonome Code-Analyse
- Findet alle Python-Files
- Zählt Lines of Code
- Extrahiert Imports
- Findet TODOs/FIXMEs
- Erstellt strukturierten Report
"""
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class FileSystemAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.tools = [
            {
                "name": "bash",
                "description": "Execute bash commands to interact with file system",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The bash command to execute"
                        }
                    },
                    "required": ["command"]
                }
            },
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
    
    def bash_tool(self, command: str) -> str:
        """Execute bash command"""
        import subprocess
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            output = result.stdout if result.stdout else result.stderr
            return output if output else "Command executed successfully (no output)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def read_file_tool(self, filepath: str) -> str:
        """Read file content"""
        try:
            # Handle relative paths
            if not os.path.isabs(filepath):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                filepath = os.path.join(base_dir, filepath)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def analyze_directory(self, directory: str) -> str:
        """
        Analysiert ein Verzeichnis mit Python-Files
        Agent arbeitet vollständig autonom
        """
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
        
        messages = [{"role": "user", "content": task}]
        
        print("🤖 FileSystem Agent gestartet...")
        print(f"📁 Analysiere: {directory}\n")
        
        iteration = 0
        max_iterations = 25
        
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Iteration {iteration}")
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )
            
            # Check stop reason
            if response.stop_reason == "end_turn":
                # Agent ist fertig
                final_text = next(
                    (block.text for block in response.content if hasattr(block, "text")),
                    None
                )
                if final_text:
                    print("\n✅ Agent fertig!\n")
                    return final_text
                else:
                    return "Agent finished but no text output found"
            
            elif response.stop_reason == "tool_use":
                # Agent nutzt Tools
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        print(f"  🔧 Tool: {tool_name}", end="")
                        
                        # Führe Tool aus
                        if tool_name == "bash":
                            cmd = block.input['command']
                            print(f" → {cmd}")
                            result = self.bash_tool(cmd)
                        elif tool_name == "read_file":
                            filepath = block.input['filepath']
                            print(f" → {filepath}")
                            result = self.read_file_tool(filepath)
                        else:
                            result = f"Unknown tool: {tool_name}"
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })
                
                # Füge Tool-Ergebnisse hinzu
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
            
            else:
                print(f"⚠️ Unexpected stop reason: {response.stop_reason}")
                break
        
        return "❌ Max iterations reached without completion"


def main():
    agent = FileSystemAgent()
    
    # Analysiere test-data Verzeichnis
    test_dir = "../test-data"
    
    print("=" * 70)
    print("🔍 FILESYSTEM AGENT - Autonome Code-Analyse")
    print("=" * 70)
    print("\n")
    
    report = agent.analyze_directory(test_dir)
    
    print("\n" + "=" * 70)
    print("📊 ANALYSIS REPORT")
    print("=" * 70)
    print("\n")
    print(report)
    
    # Speichere Report
    output_file = "analysis_report.md"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "=" * 70)
    print(f"✅ Report gespeichert: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()