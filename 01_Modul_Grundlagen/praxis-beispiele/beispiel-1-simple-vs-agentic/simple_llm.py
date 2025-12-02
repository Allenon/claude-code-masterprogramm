# simple_llm.py
"""
Simple LLM Call ohne Tool-Zugriff
Demonstriert die Limitierung traditioneller LLM-Calls
"""
import anthropic
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()

def simple_llm_call():
    """
    Einfacher LLM Call ohne Tools
    Kann NICHT auf das Dateisystem zugreifen
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    print("=== SIMPLE LLM (ohne Tools) ===")
    print("Frage: 'Liste alle Python-Dateien im aktuellen Verzeichnis auf'\n")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user", 
                "content": "Liste alle Python-Dateien im aktuellen Verzeichnis auf und zeige ihre Größe."
            }
        ]
    )
    
    print("Antwort:")
    print(message.content[0].text)
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    simple_llm_call()