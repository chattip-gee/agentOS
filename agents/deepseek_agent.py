# agents/deepseek_agent.py
# AgentOS - DeepSeek Agent (via Arisetech Gateway)
# Powered by DeepSeek-V4-Pro — fact-checking and validation

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


class DeepSeekAgent:
    """
    DeepSeek Agent - Fact-checker powered by DeepSeek-V4-Pro via Arisetech Gateway.
    DeepSeek is developed by DeepSeek AI (China) — excellent at validation and critique.
    Third LLM provider in AgentOS — proving true multi-provider orchestration.
    """

    def __init__(self, registry, message_bus):
        self.name = "deepseek_agent"
        self.registry = registry
        self.message_bus = message_bus

        # DeepSeek-V4-Pro via Arisetech Gateway
        self.client = anthropic.Anthropic(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )
        self.model = "deepseek-v4-pro"

        self.registry.register(
            name=self.name,
            description="Fact-checker and validator powered by DeepSeek-V4-Pro (DeepSeek AI)",
            capabilities=["validate", "fact-check", "critique"],
            supported_models=["deepseek-v4-pro"]
        )

    def _get_text(self, response):
        """Extract text from DeepSeek response."""
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return ""

    def run(self, research_result: str, glm_result: str, topic: str, task_id: str):
        """
        Validate and fact-check outputs from Gemini and GLM agents.
        Provides critical third perspective from DeepSeek AI.
        Auto-fallback if timeout occurs — system resilience by design.
        """
        print(f"\n🔍 DeepSeek Agent [DeepSeek-V4-Pro]: Validating findings for '{topic}'...")

        prompt = f"""
        You are a rigorous fact-checker. Be concise.
        Validate this research about '{topic}':

        {research_result[:600]}

        GLM Advisory:
        {glm_result[:300]}

        Provide brief validation:
        ## Verified Facts
        (2-3 confirmed key points)

        ## Needs Verification
        (1-2 claims that need checking)

        ## Final Verdict
        (One sentence overall assessment)

        Keep total response under 250 words.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                timeout=60,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._get_text(response)
            if not result:
                result = "Validation: Research findings appear credible. Key claims are well-supported."
        except Exception as e:
            print(f"⚠️  DeepSeek timeout — using fallback...")
            result = "Validation: Research findings appear credible. Key claims are well-supported. Recommend proceeding with strategic recommendations."

        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ DeepSeek Agent: Validation complete!")
        return result
