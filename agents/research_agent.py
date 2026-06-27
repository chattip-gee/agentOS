# agents/research_agent.py
# AgentOS - Research Agent
# Powered by Gemini 2.5 Flash — best for research and information gathering

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class ResearchAgent:
    """
    Research Agent - The information gatherer of AgentOS.
    Powered by Gemini 2.5 Flash for fast, accurate research.
    """

    def __init__(self, registry, message_bus):
        self.name = "research_agent"
        self.registry = registry
        self.message_bus = message_bus

        # Gemini is best for research tasks
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "gemini-2.5-flash-lite"

        self.registry.register(
            name=self.name,
            description="Researches and analyzes topics using Gemini 2.5 Flash",
            capabilities=["research", "analyze", "summarize"],
            supported_models=["gemini-2.5-flash-lite"]
        )

    def run(self, topic: str, task_id: str):
        """Research a topic and return key findings."""
        print(f"\n🔍 Research Agent [Gemini]: Analyzing '{topic}'...")

        prompt = f"""
        You are an expert research analyst.
        Research the following topic thoroughly: {topic}

        Provide your analysis in this structure:
        1. OVERVIEW: Brief summary of the topic
        2. KEY FINDINGS: 3-5 most important insights
        3. CHALLENGES: Main problems or obstacles
        4. OPPORTUNITIES: Potential solutions or advantages
        5. CONCLUSION: Key takeaway for decision makers

        Be concise, factual, and insightful.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        result = response.text

        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Research Agent: Analysis complete!")
        return result
