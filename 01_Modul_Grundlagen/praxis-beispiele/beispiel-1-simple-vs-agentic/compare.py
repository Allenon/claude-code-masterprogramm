# compare.py
"""
Vergleicht Simple LLM vs. Agentic Agent Side-by-Side
"""
import simple_llm
import agentic_agent

def main():
    print("\n" + "="*60)
    print("VERGLEICH: Simple LLM vs. Agentic Agent")
    print("="*60 + "\n")
    
    # 1. Simple LLM
    print("1️⃣  SIMPLE LLM (ohne Tools)")
    print("-"*60)
    simple_llm.simple_llm_call()
    
    input("Drücke Enter für Agentic Agent...\n")
    
    # 2. Agentic Agent
    print("2️⃣  AGENTIC AGENT (mit Tools)")
    print("-"*60)
    agentic_agent.agentic_agent_call()
    
    print("="*60)
    print("🎯 FAZIT:")
    print("="*60)
    print("❌ Simple LLM: Kann nur 'vermuten' - keine echten Daten")
    print("✅ Agentic Agent: Führt Commands aus - liefert echte Ergebnisse")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()