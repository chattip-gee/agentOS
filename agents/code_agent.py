# agents/code_agent.py
# AgentOS - Code Agent
# Helps developers write code, fix bugs, review code, and understand concepts

import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()


class CodeAgent:
    """
    Code Agent - The developer assistant of AgentOS.
    Intelligently detects what the developer needs and responds accordingly.
    Handles: code writing, bug fixing, code explanation, code review, test writing.
    """

    def __init__(self, registry, message_bus):
        self.name = "code_agent"
        self.registry = registry
        self.message_bus = message_bus

        # Initialize Gemini client
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Register this agent into AgentOS
        self.registry.register(
            name=self.name,
            description="Helps developers write code, fix bugs, review and explain concepts",
            capabilities=["code", "debug", "explain", "review", "test"]
        )

    def _detect_intent(self, request: str) -> str:
        """
        Detect what the developer actually needs.
        Uses Gemini to classify the request into one of five intents:
        - write:   user wants new code written from scratch
        - debug:   user wants a bug fixed or error explained
        - explain: user wants a concept or code explained
        - review:  user wants existing code reviewed
        - test:    user wants unit tests written
        """
        prompt = f"""
        Analyze this developer request and classify it into exactly ONE category:
        - write:   user wants new code written
        - debug:   user wants a bug fixed or error explained
        - explain: user wants a concept or code explained
        - review:  user wants code reviewed for quality/issues
        - test:    user wants unit tests written

        Request: {request}

        Reply with ONLY one word (write, debug, explain, review, or test).
        No punctuation, no explanation.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        intent = response.text.strip().lower()

        # Fallback to 'write' if unrecognized
        if intent not in ["write", "debug", "explain", "review", "test"]:
            intent = "write"

        return intent

    def _build_prompt(self, intent: str, request: str) -> str:
        """
        Build a targeted prompt based on the detected intent.
        Each intent gets a specialized prompt for best results.
        """

        if intent == "debug":
            return f"""
            You are an expert debugger and senior software engineer.
            A developer needs help fixing a bug or understanding an error.

            Request: {request}

            Provide a structured response:

            # Bug Analysis

            ## What's Wrong
            (Clear explanation of the problem in plain English)

            ## Root Cause
            (Why this error occurs technically)

            ## Fixed Code
            ```python
            # Complete fixed code here with comments
            ```

            ## Why This Fix Works
            (Explanation of the solution)

            ## How to Prevent This
            (Best practices to avoid this issue in future)
            """

        elif intent == "explain":
            return f"""
            You are an expert teacher and senior software engineer.
            Explain this concept or code clearly for a developer.

            Request: {request}

            Provide a structured response:

            # Explanation: [Topic Name]

            ## Simple Summary
            (1-2 sentences in plain English — no jargon)

            ## How It Works
            (Step-by-step breakdown)

            ## Code Example
            ```python
            # Clear, minimal working example
            ```

            ## Real-World Use Cases
            (When and why developers use this)

            ## Key Takeaway
            (The single most important thing to remember)
            """

        elif intent == "review":
            return f"""
            You are a senior software engineer conducting a thorough code review.

            Request: {request}

            Provide a structured response:

            # Code Review Report

            ## Overall Assessment
            (One line summary: Excellent / Good / Needs Improvement / Critical Issues)

            ## Strengths
            (What the code does well)

            ## Issues Found
            Rank each issue by severity:
            - 🔴 Critical: Must fix before production
            - 🟡 Warning: Should fix soon
            - 🔵 Suggestion: Nice to have improvement

            ## Refactored Code
            ```python
            # Improved version with comments explaining changes
            ```

            ## Summary of Improvements
            (Key changes made and why)
            """

        elif intent == "test":
            return f"""
            You are an expert in software testing, TDD, and pytest.

            Request: {request}

            Provide a structured response:

            # Test Suite

            ## Test Strategy
            (What we're testing and why — unit, integration, edge cases)

            ## Test Code
            ```python
            # Complete pytest test suite
            # Include: happy path, edge cases, error cases
            ```

            ## Edge Cases Covered
            (List of all edge cases included in tests)

            ## How to Run
            ```bash
            # Command to install pytest and run tests
            ```
            """

        else:  # write
            return f"""
            You are an expert software engineer.
            Write clean, production-ready code for this request.

            Request: {request}

            Provide a structured response:

            # Solution: [Brief Title]

            ## Approach
            (Brief explanation of the approach and why it was chosen)

            ## Code
            ```python
            # Complete, working, well-commented production-ready code
            ```

            ## Usage Example
            ```python
            # How to use this code with example inputs and outputs
            ```

            ## Key Features
            (What makes this implementation good)

            ## Possible Improvements
            (Optional enhancements for future consideration)
            """

    def run(self, request: str, task_id: str) -> str:
        """
        Process a developer request intelligently.
        1. Detect intent (write/debug/explain/review/test)
        2. Build targeted prompt
        3. Generate response with Gemini
        4. Store result in message bus
        """
        print(f"\n💻 Code Agent: Processing developer request...")

        # Step 1: Detect what the developer needs
        intent = self._detect_intent(request)
        intent_emoji = {
            "write": "✍️",
            "debug": "🐛",
            "explain": "📖",
            "review": "🔍",
            "test": "🧪"
        }
        print(f"{intent_emoji.get(intent, '💡')} Detected intent: {intent.upper()}")

        # Step 2: Build targeted prompt
        prompt = self._build_prompt(intent, request)

        # Step 3: Generate response using Gemini
        print(f"🤖 Generating {intent} response...")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text

        # Step 4: Store result in message bus for audit trail
        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Code Agent: {intent.capitalize()} complete!")
        return result
