# research_agent.py
"""
Research Agent: Autonome Recherche und Report-Erstellung

UNTERSCHIED ZU BEISPIEL 2:
- FileSystem Agent: Lokale Files analysieren
- Research Agent: Informationen sammeln, synthetisieren, strukturieren

PRODUCTION USE CASE:
- Competitive Analysis
- Technology Research  
- Market Intelligence

HINWEIS:
In Production würde dieser Agent echte web_search/web_fetch Tools nutzen.
Für das Training simulieren wir Recherche - Fokus liegt auf Agent-Logik.
"""
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()


class ResearchAgent:
    def __init__(self):
        """
        Initialisiert Research Agent
        
        In Production: Würde web_search und web_fetch Tools haben
        Im Training: Simulieren wir mit research_topic Tool
        """
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Tool Definition
        # In Production: web_search, web_fetch statt research_topic
        self.tools = [
            {
                "name": "research_topic",
                "description": "Simulate research on a given topic. Returns structured information.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic to research"
                        },
                        "focus": {
                            "type": "string",
                            "description": "Specific aspect to focus on",
                            "enum": ["overview", "technical", "business", "comparison"]
                        }
                    },
                    "required": ["topic"]
                }
            }
        ]
    
    def research_topic_tool(self, topic: str, focus: str = "overview") -> str:
        """
        Simuliert Recherche-Ergebnis
        
        In Production: Würde echte web_search API aufrufen
        Im Training: Gibt strukturierte Mock-Daten zurück
        
        WICHTIG: Das Konzept bleibt gleich - nur die Datenquelle ändert sich
        """
        
        # Mock-Daten für bekannte Topics
        mock_research = {
            "Anthropic Model Context Protocol": {
                "overview": """
Model Context Protocol (MCP) by Anthropic:
- Universal protocol for connecting AI assistants to data sources
- Released November 2024
- Open-source, community-driven
- Enables standardized tool integration
- Key components: Clients, Servers, Resources, Tools
- Similar to LSP (Language Server Protocol) but for AI
- Enables agents to connect to databases, APIs, file systems
                """,
                "technical": """
Technical Architecture of MCP:
- JSON-RPC 2.0 based protocol
- Bidirectional communication
- Supports stdio, HTTP/SSE transports
- TypeScript and Python SDKs available
- Server can expose: Resources, Tools, Prompts
- Client discovery mechanism for capabilities
- Stateful sessions with context management
- Security: Authentication and authorization built-in
                """,
                "business": """
Business Impact of MCP:
- Reduces integration complexity (one protocol vs many APIs)
- Lower maintenance overhead for enterprises
- Faster time-to-market for AI features
- Growing ecosystem of MCP servers (Slack, GitHub, Google Drive, etc.)
- Enterprise adoption increasing rapidly
- Cost reduction through standardization
- Vendor-agnostic approach reduces lock-in
                """,
                "comparison": """
MCP vs Traditional Integration:
- Traditional: Custom API integration for each service (high complexity)
- MCP: Single protocol, multiple services (low complexity)
- Traditional: Separate auth, data formats, error handling per service
- MCP: Standardized across all services
- Similar evolution to USB (one port, many devices)
                """
            },
            "Agentic AI": {
                "overview": """
Agentic AI Overview:
- AI systems that can act autonomously to achieve goals
- Key capabilities: Planning, Tool Use, Memory, Reflection
- Differs from traditional LLMs: Passive response vs Active agent
- Use cases: Automation, Analysis, Orchestration, Decision-making
- Major players: Anthropic (Claude), OpenAI (GPT with tools), Google (Gemini)
                """,
                "technical": """
Technical Components of Agentic AI:
- Planning Engine: Breaks down tasks into steps
- Tool Integration: Access to external APIs and functions
- Memory Systems: Short-term (conversation) and long-term (vector DBs)
- Reasoning Loop: Observe → Plan → Act → Reflect → Repeat
- Error Handling: Retry logic, fallbacks, validation
- State Management: Tracks progress across iterations
                """,
                "business": """
Business Applications of Agentic AI:
- Customer Support: Autonomous ticket resolution
- DevOps: Automated incident response and debugging
- Sales: Lead qualification and outreach
- Research: Market analysis and competitive intelligence
- Finance: Automated reporting and analysis
- HR: Resume screening and candidate outreach
- ROI: 40-60% reduction in manual tasks
                """,
                "comparison": """
Agentic AI vs Traditional AI:
- Traditional LLM: Input → Output (static, one-shot)
- Agentic AI: Goal → Plan → Execute → Adapt (dynamic, iterative)
- Traditional: No tool use, no memory
- Agentic: Full tool access, persistent memory
- Traditional: Human drives each step
- Agentic: AI drives entire workflow
- Example: ChatGPT (traditional) vs Claude Code (agentic)
                """
            },
            "Claude Code": {
                "overview": """
Claude Code Overview:
- Command-line AI coding assistant by Anthropic
- Agentic approach: Can execute commands, read files, write code
- Direct access to development environment
- Integration with git, package managers, build tools
- Context-aware: Understands entire codebase
                """,
                "technical": """
Claude Code Technical Details:
- Built on Claude Sonnet 4 model
- Computer Use capability: bash, file operations
- Model Context Protocol (MCP) integration
- Long context window: 200K tokens
- Streaming responses for real-time feedback
- Tool orchestration: Can use multiple tools in parallel
                """,
                "comparison": """
Claude Code vs GitHub Copilot:
- Copilot: Code completion, inline suggestions
- Claude Code: Full agent, can execute and test
- Copilot: IDE integration (VS Code, JetBrains)
- Claude Code: Terminal-based, IDE-agnostic
- Copilot: Reactive (suggests as you type)
- Claude Code: Proactive (understands and executes tasks)
                """
            }
        }
        
        # Suche nach passendem Mock-Result
        for key in mock_research:
            if key.lower() in topic.lower():
                return mock_research[key].get(focus, mock_research[key]["overview"])
        
        # Fallback für unbekannte Topics
        return f"""
Research simulation for '{topic}' (focus: {focus})

In production, this would return real web search results from:
- Academic papers
- Technical documentation
- Industry reports
- News articles
- Expert blogs

The agent would then synthesize this information into a structured report.
"""
    
    def research(self, topic: str, depth: str = "standard") -> str:
        """
        Führt autonome Recherche durch
        
        AGENT ENTSCHEIDET:
        - Welche Aspekte recherchieren
        - Welcher Focus für jeden Aspekt
        - Wie Informationen strukturieren
        - Wann genug Information vorliegt
        
        PARAMETER:
        - topic: Das zu recherchierende Thema
        - depth: quick | standard | deep (beeinflusst Anzahl Tool-Calls)
        """
        
        task = f"""
Recherchiere umfassend zum Thema: {topic}

Vorgehen:
1. Identifiziere die wichtigsten Aspekte des Themas
2. Recherchiere jeden Aspekt systematisch
3. Nutze verschiedene Focus-Parameter (overview, technical, business, comparison)
4. Synthetisiere alle Informationen zu einem kohärenten Report

Erstelle einen finalen Report im Markdown-Format mit folgender Struktur:

# {topic}

## Executive Summary
[2-3 Sätze, die das Wichtigste zusammenfassen]

## Haupterkenntnisse
[3-5 Key Points als Bullet Points]

## Detaillierte Analyse
[Strukturierte Analyse der recherchierten Aspekte]

## Quellen/Basis
[Kurze Erwähnung der recherchierten Aspekte]

Recherche-Tiefe: {depth}
Sei gründlich und nutze die verfügbaren Tools systematisch.
"""
        
        messages = [{"role": "user", "content": task}]
        
        print(f"🔍 Research Agent gestartet")
        print(f"📌 Thema: {topic}")
        print(f"📊 Tiefe: {depth}\n")
        
        iteration = 0
        max_iterations = 15
        
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Iteration {iteration}")
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )
            
            if response.stop_reason == "end_turn":
                # Agent ist fertig
                final_text = next(
                    (block.text for block in response.content if hasattr(block, "text")),
                    None
                )
                if final_text:
                    print("\n✅ Research abgeschlossen\n")
                    return final_text
                return "Research finished without text output"
            
            elif response.stop_reason == "tool_use":
                # Agent möchte Tool nutzen
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        topic_query = block.input.get('topic', '')
                        focus = block.input.get('focus', 'overview')
                        
                        print(f"  🔧 Tool: {tool_name}")
                        print(f"     Query: {topic_query}")
                        print(f"     Focus: {focus}")
                        
                        # Führe Tool aus
                        result = self.research_topic_tool(topic_query, focus)
                        
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
            
            else:
                print(f"⚠️ Unexpected stop reason: {response.stop_reason}")
                break
        
        return "❌ Max iterations reached without completion"


def main():
    """
    Main Function: Testet Research Agent mit verschiedenen Topics
    """
    agent = ResearchAgent()
    
    # Test-Topics mit unterschiedlichen Schwierigkeitsgraden
    topics = [
        ("Anthropic Model Context Protocol", "standard"),
        ("Agentic AI Design Patterns", "standard"),
    ]
    
    print("=" * 70)
    print("🔍 RESEARCH AGENT - Autonome Recherche")
    print("=" * 70)
    print("\n")
    
    for i, (topic, depth) in enumerate(topics, 1):
        print(f"\n📝 Research {i}/{len(topics)}")
        print("-" * 70)
        
        # Führe Recherche durch
        report = agent.research(topic, depth)
        
        # Zeige Report
        print("\n" + "=" * 70)
        print("📊 RESEARCH REPORT")
        print("=" * 70)
        print("\n")
        print(report)
        
        # Speichere Report als Markdown
        filename = f"research_{i}_{topic.replace(' ', '_')[:30]}.md"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(f"# Research Report: {topic}\n\n")
            f.write(f"**Generated by Research Agent**\n\n")
            f.write(f"---\n\n")
            f.write(report)
        
        print("\n" + "=" * 70)
        print(f"✅ Report gespeichert: {filename}")
        print("=" * 70)
        
        # Pause zwischen Topics
        if i < len(topics):
            input("\nDrücke Enter für nächste Recherche...\n")


if __name__ == "__main__":
    main()