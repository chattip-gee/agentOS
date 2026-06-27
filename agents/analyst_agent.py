# agents/analyst_agent.py
# AgentOS - Analyst Agent
# Responsible for deep analysis and generating actionable insights

import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

class AnalystAgent:
    """
    Analyst Agent - The strategic thinker of AgentOS.
    Takes research findings and produces actionable insights and recommendations.
    """

    def __init__(self, registry, message_bus):
        self.name = "analyst_agent"
        self.registry = registry
        self.message_bus = message_bus

        # Initialize Gemini client
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Register this agent into the system
        self.registry.register(
            name=self.name,
            description="Analyzes research findings and generates strategic insights",
            capabilities=["analyze", "strategize", "recommend"]
        )

    def run(self, research_result: str, topic: str, task_id: str):
        """
        Analyze research findings and produce strategic recommendations.
        research_result: output from Research Agent
        topic: original topic being investigated
        task_id: unique task identifier for tracking
        """
        print(f"\n📊 Analyst Agent: Generating insights for '{topic}'...")

        # Craft a strategic analysis prompt
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

        # Call Gemini API
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        result = response.text

        # Store result in message bus
        self.message_bus.store_result(
            agent_name=self.name,
            task_id=task_id,
            result=result
        )

        print(f"✅ Analyst Agent: Strategic insights complete!")
        return result