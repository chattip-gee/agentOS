# agents/code_agent.py
# AgentOS - Code Agent
# Powered by DeepSeek-V4-Pro — best for code tasks

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


class CodeAgent:
    """
    Code Agent - Developer assistant powered by DeepSeek-V4-Pro.
    DeepSeek excels at code writing, debugging, and technical explanation.
    Handles: write, debug, explain, review, test.
    """

    def __init__(self, registry, message_bus):
        self.name = "code_agent"
        self.registry = registry
        self.message_bus = message_bus

        # DeepSeek is best for code tasks
        self.client = anthropic.Anthropic(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("ANTHROPIC_BASE_URL")
        )
        self.model = "deepseek-v4-pro"

        self.registry.register(
            name=self.name,
            description="Developer assistant powered by DeepSeek-V4-Pro",
            capabilities=["code", "debug", "explain", "review", "test"],
            supported_models=["deepseek-v4-pro"]
        )

    def _get_text(self, response):
        """Extract text from DeepSeek response."""
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return ""

    def _detect_intent(self, request: str) -> str:
        """Detect what the developer needs."""
        prompt = f"""
        Classify this developer request into ONE category:
        - write: user wants new code written
        - debug: user wants a bug fixed or error explained
        - explain: user wants a concept or code explained
        - review: user wants code reviewed
        - test: user wants tests written

        Request: {request}

        Reply with ONLY one word.
        """

        response = self.client.messages.create(
            model=self.model,
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )

        intent = self._get_text(response).strip().lower()
        if intent not in ["write", "debug", "explain", "review", "test"]:
            intent = "write"
        return intent

    def _build_prompt(self, intent: str, request: str) -> str:
        """Build targeted prompt based on detected intent."""

        if intent == "debug":
            return f"""
            You are an expert debugger.
            Request: {request}

            # Bug Analysis
            ## What's Wrong
            ## Root Cause
            ## Fixed Code
            ```python
            ```
            ## Why This Fix Works
            ## How to Prevent This
            """
        elif intent == "explain":
            return f"""
            You are an expert teacher.
            Request: {request}

            # Explanation
            ## Simple Summary
            ## How It Works
            ## Code Example
            ```python
            ```
            ## Real-World Use Cases
            ## Key Takeaway
            """
        elif intent == "review":
            return f"""
            You are a senior software engineer doing code review.
            Request: {request}

            # Code Review Report
            ## Overall Assessment
            ## Strengths
            ## Issues Found (Critical / Warning / Suggestion)
            ## Refactored Code
            ```python
            ```
            ## Summary of Improvements
            """
        elif intent == "test":
            return f"""
            You are an expert in software testing.
            Request: {request}

            # Test Suite
            ## Test Strategy
            ## Test Code
            ```python
            ```
            ## Edge Cases Covered
            ## How to Run
            """
        else:
            return f"""
            You are an expert software engineer.
            Request: {request}

            # Solution
            ## Approach
            ## Code
            ```python
            ```
            ## Usage Example
            ```python
            ```
            ## Key Features
            """

    def run(self, request: str, task_id: str) -> str:
        """Process developer request intelligently."""
        print(f"\n💻 Code Agent [DeepSeek]: Processing developer request...")

        intent = self._detect_intent(request)
        intent_emoji = {
            "write": "✍️", "debug": "🐛",
            "explain": "📖", "review": "🔍", "test": "🧪"
        }
        print(f"{intent_emoji.get(intent, '💡')} Detected intent: {intent.upper()}")

        prompt = self._build_prompt(intent, request)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = self._get_text(response)

        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Code Agent: {intent.capitalize()} complete!")
        return result
