# agents/glm_agent.py
# AgentOS - GLM Agent (via Arisetech Gateway)
# Powered by GLM-5.1 — strategic advisory with deep reasoning

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


class GLMAgent:
    """
    GLM Agent - Strategic advisor powered by GLM-5.1 via Arisetech Gateway.
    GLM-5.1 is developed by Zhipu AI (China) — brings diverse AI perspective.
    Demonstrates AgentOS running agents from different global LLM providers.
    """

    def __init__(self, registry, message_bus):
        self.name = "glm_agent"
        self.registry = registry
        self.message_bus = message_bus

        # GLM-5.1 via Arisetech Gateway
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )
        self.model = "glm-5.1"

        self.registry.register(
            name=self.name,
            description="Strategic advisor powered by GLM-5.1 (Zhipu AI)",
            capabilities=["advise", "critique", "validate"],
            supported_models=["glm-5.1"]
        )

    def _get_text(self, response):
        """Extract text from GLM response (handles ThinkingBlock)."""
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return ""

    def run(self, research_result: str, topic: str, task_id: str):
        """
        Provide strategic advisory using GLM-5.1.
        GLM brings a different perspective as a non-Western LLM provider.
        """
        print(f"\n🤖 GLM Agent [GLM-5.1 / Zhipu AI]: Advising on '{topic}'...")

        prompt = f"""
        You are a strategic advisor with deep expertise in business and technology.
        Review this research about '{topic}' and provide your expert perspective.

        Research findings:
        {research_result}

        Provide:
        # Strategic Advisory: {topic}

        ## Critical Assessment
        (What's most important and what might be overlooked)

        ## Key Opportunities
        (Top 3 opportunities worth pursuing immediately)

        ## Risk Factors
        (Critical risks that need attention)

        ## Advisory Recommendation
        (Your single most important recommendation)

        Be direct, insightful, and actionable.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                timeout=90,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._get_text(response)
        except Exception as e:
            print(f"⚠️  GLM timeout/error, recording partial result...")
            result = f"GLM Advisory unavailable: {str(e)[:100]}"

        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ GLM Agent: Strategic advisory complete!")
        return result
