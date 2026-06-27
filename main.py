# main.py
# AgentOS - Main Orchestrator
# Coordinates multiple AI agents across different LLM providers

import uuid
from core.registry import AgentRegistry
from core.message_bus import MessageBus
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent
from agents.glm_agent import GLMAgent
from agents.deepseek_agent import DeepSeekAgent
from agents.code_agent import CodeAgent
from tools.drive_tool import DriveTool


def run_agentos(topic: str, mode: str = "research"):
    """
    Main AgentOS pipeline.
    Orchestrates agents across Gemini, GLM, and DeepSeek providers.
    mode: 'research' for market research, 'developer' for code help
    """

    print("\n" + "="*60)
    print("🤖 AgentOS: The Operating System for AI Agents")
    print("🌍 Providers: Gemini (Google) + GLM (Zhipu AI) + DeepSeek")
    print("="*60)

    # Generate unique task ID for tracking
    task_id = str(uuid.uuid4())[:8]
    print(f"\n📋 Task ID: {task_id}")
    print(f"📌 Request: {topic}")
    print(f"🎯 Mode: {mode}\n")

    # Step 1: Initialize core components
    print("🔧 Initializing AgentOS core components...")
    registry = AgentRegistry()
    message_bus = MessageBus()

    # Step 2: Initialize MCP Google Drive Tool
    print("☁️  Connecting to Google Drive via MCP...")
    drive_tool = DriveTool()
    print("✅ Google Drive MCP connected!\n")

    # Step 3: Register and run agents based on selected mode
    print("🔧 Registering agents into AgentOS...\n")

    if mode == "developer":
        # Developer mode — Code Agent powered by DeepSeek
        code_agent = CodeAgent(registry, message_bus)
        registry.list_agents()

        print("="*60)
        print("🚀 AgentOS: Starting developer pipeline...")
        print("="*60)

        final_report = code_agent.run(
            request=topic,
            task_id=task_id
        )

    else:
        # Research mode — Multi-provider pipeline
        # Gemini → Research | DeepSeek → Analysis | GLM → Advisory | Gemini → Write
        research_agent = ResearchAgent(registry, message_bus)
        analyst_agent = AnalystAgent(registry, message_bus)
        glm_agent = GLMAgent(registry, message_bus)
        deepseek_agent = DeepSeekAgent(registry, message_bus)
        writer_agent = WriterAgent(registry, message_bus)
        registry.list_agents()

        print("="*60)
        print("🚀 AgentOS: Starting multi-provider pipeline...")
        print("="*60)

        # Step 1: Gemini researches the topic
        research_result = research_agent.run(
            topic=topic,
            task_id=task_id
        )

        # Step 2: DeepSeek analyzes strategically
        analysis_result = analyst_agent.run(
            research_result=research_result,
            topic=topic,
            task_id=task_id
        )

        # Step 3: GLM provides strategic advisory
        glm_result = glm_agent.run(
            research_result=research_result,
            topic=topic,
            task_id=task_id
        )

        # Step 4: DeepSeek validates all findings
        deepseek_result = deepseek_agent.run(
            research_result=research_result,
            glm_result=glm_result,
            topic=topic,
            task_id=task_id
        )

        # Step 5: Gemini synthesizes everything into final report
        final_report = writer_agent.run(
            research_result=research_result,
            analysis_result=analysis_result + "\n\n" + glm_result + "\n\n" + deepseek_result,
            topic=topic,
            task_id=task_id
        )

    # Display final report
    print("\n" + "="*60)
    print("📄 FINAL REPORT")
    print("="*60)
    print(final_report)

    # Save to Google Drive via MCP
    drive_link = drive_tool.save_report(
        filename=f"AgentOS_{mode}_Report",
        content=final_report,
        task_id=task_id
    )

    # Show audit trail
    print("\n" + "="*60)
    print("📨 AgentOS Message History (Audit Trail)")
    print("="*60)
    for msg in message_bus.get_history():
        print(f"  {msg['timestamp']} | {msg['sender']} → {msg['receiver']}")

    print("\n" + "="*60)
    print("✅ AgentOS Pipeline Complete!")
    print(f"📁 Report saved to Google Drive: {drive_link}")
    print("="*60)

    return final_report


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 Welcome to AgentOS")
    print("    The Operating System for AI Agents")
    print("    Powered by Gemini + GLM + DeepSeek")
    print("="*60)

    # Select mode
    print("\n🎯 Select Mode:")
    print("  1. Research Mode  — Multi-provider market research & analysis")
    print("  2. Developer Mode — Code writing, bug fixing & explanation")
    print()
    mode_input = input("Enter mode (1 or 2): ").strip()

    if mode_input == "2":
        mode = "developer"
        print("\n💻 Developer Mode — What can I help you with?")
        print()
        print("Examples:")
        print("  • Write a Python function to read a CSV and return statistics")
        print("  • Fix this bug: IndexError list index out of range")
        print("  • Explain how async/await works in Python")
        print("  • Review my code: [paste your code here]")
        print("  • Write unit tests for a login function")
    else:
        mode = "research"
        print("\n🌏 Research Mode — What would you like to research?")
        print()
        print("Examples:")
        print("  • AI Agent technology trends in Japan 2025")
        print("  • Best practices for building production-ready AI agents")
        print("  • How SMEs can leverage AI agents to compete globally")
        print("  • Future of multi-agent systems in enterprise 2025")
        print("  • Electric vehicle market opportunities in Southeast Asia")

    print()
    topic = input("Enter your request: ").strip()

    if not topic:
        if mode == "developer":
            topic = "Write a Python function to read a CSV file and return summary statistics"
        else:
            topic = "AI Agent technology trends and opportunities in Japan 2025"
        print(f"\n⚠️  No input detected. Using default example:")
        print(f"    {topic}")

    run_agentos(topic, mode)
