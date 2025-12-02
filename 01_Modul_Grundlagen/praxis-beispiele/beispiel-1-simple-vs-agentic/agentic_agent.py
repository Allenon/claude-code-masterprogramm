# agentic_agent.py
"""
Agentic Agent mit Tool-Zugriff
Kann eigenständig bash commands ausführen
"""
import anthropic
import os
import subprocess
from dotenv import load_dotenv

# Load API Key
load_dotenv()

def bash_tool(command: str) -> str:
    """Execute bash command and return output"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=10
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

def agentic_agent_call():
    """
    Agentic Agent mit Tool-Zugriff
    Kann eigenständig bash commands ausführen
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Definiere Tools
    tools = [
        {
            "name": "bash",
            "description": "Execute bash commands to interact with the file system",
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
        }
    ]
    
    # Initial Request
    messages = [
        {
            "role": "user",
            "content": "Liste alle Python-Dateien im aktuellen Verzeichnis auf und zeige ihre Größe."
        }
    ]
    
    print("=== AGENTIC AGENT (mit Tools) ===")
    print("Frage: 'Liste alle Python-Dateien im aktuellen Verzeichnis auf'\n")
    print("Agent Loop startet...\n")
    
    # Agent Loop
    iteration = 0
    while True:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )
        
        print(f"Stop reason: {response.stop_reason}")
        
        # Verarbeite Response
        if response.stop_reason == "end_turn":
            # Agent ist fertig
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                None
            )
            if final_text:
                print(f"\n✅ Final Answer:\n{final_text}")
            break
        
        elif response.stop_reason == "tool_use":
            # Agent möchte Tool nutzen
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Tool: {block.name}")
                    print(f"   Command: {block.input['command']}")
                    
                    # Führe Tool aus
                    result = bash_tool(block.input['command'])
                    print(f"   Result: {result}")
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            # Füge Tool-Ergebnisse zu Messages hinzu
            messages.append({
                "role": "user",
                "content": tool_results
            })
        
        if iteration > 10:
            print("⚠️ Max iterations reached!")
            break
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    agentic_agent_call()