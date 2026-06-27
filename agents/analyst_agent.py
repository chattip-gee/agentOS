# agents/analyst_agent.py
# AgentOS - Analyst Agent
# Powered by DeepSeek-V4-Pro — best for deep reasoning and strategic analysis

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


class AnalystAgent:
    """
    Analyst Agent - The strategic thinker of AgentOS.
    Powered by DeepSeek-V4-Pro for deep reasoning and strategic analysis.
    """

    def __init__(self, registry, message_bus):
        self.name = "analyst_agent"
        self.registry = registry
        self.message_bus = message_bus

        # DeepSeek is best for strategic analysis and reasoning
        self.client = anthropic.Anthropic(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )
        self.model = "deepseek-v4-pro"

        self.registry.register(
            name=self.name,
            description="Analyzes findings and generates strategic insights using DeepSeek-V4-Pro",
            capabilities=["analyze", "strategize", "recommend"],
            supported_models=["deepseek-v4-pro"]
        )

    def _get_text(self, response):
        """Extract text from DeepSeek response."""
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return ""

    def run(self, research_result: str, topic: str, task_id: str):
        """Analyze research findings and produce strategic recommendations."""
        print(f"\n📊 Analyst Agent [DeepSeek]: Generating insights for '{topic}'...")

        prompt = f"""
        You are a senior strategic analyst.
        Based on the following research about '{topic}':

        {research_result}

        Provide a strategic analysis with this structure:
        1. STRATEGIC ASSESSMENT: Overall evaluation of the situation
        2. RISK ANALYSIS: Top 3 risks to consider
        3. STRATEGIC RECOMMENDATIONS: 3 concrete actions to take
        4. SUCCESS METRICS: How to measure success
        5. PRIORITY ACTION: The single most important thing to do first

        Focus on actionable insights that drive real business value.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        result = self._get_text(response)

        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Analyst Agent: Strategic insights complete!")
        return result
