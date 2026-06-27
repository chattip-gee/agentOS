# agents/research_agent.py
# AgentOS - Research Agent
# Responsible for gathering and analyzing information using Gemini AI

import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

class ResearchAgent:
    """
    Research Agent - The information gatherer of AgentOS.
    Analyzes topics and extracts key insights using Gemini AI.
    """

    def __init__(self, registry, message_bus):
        self.name = "research_agent"
        self.registry = registry
        self.message_bus = message_bus

        # Initialize Gemini client
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Register this agent into the system
        self.registry.register(
            name=self.name,
            description="Researches and analyzes topics using Gemini AI",
            capabilities=["research", "analyze", "summarize"]
        )

    def run(self, topic: str, task_id: str):
        """
        Research a given topic and return key findings.
        topic: the subject to research
        task_id: unique task identifier for tracking
        """
        print(f"\n🔍 Research Agent: Analyzing '{topic}'...")

        # Craft a structured prompt for deep research
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

        # Call Gemini API
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text

        # Store result in message bus for other agents to use
        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Research Agent: Analysis complete!")
        return result