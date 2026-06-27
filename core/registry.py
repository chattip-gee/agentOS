# core/registry.py
# AgentOS - Agent Registry
# Manages registration and discovery of all agents in the system

class AgentRegistry:
    """
    Central registry for all AgentOS agents.
    Every agent must register here before participating in task execution.
    """
    
    def __init__(self):
        # Dictionary storing all registered agents
        # key = agent name, value = agent metadata
        self.agents = {}
    
    def register(self, name: str, description: str, capabilities: list):
        """
        Register a new agent into the system.
        name: unique agent identifier e.g. 'research_agent'
        description: what this agent does
        capabilities: list of skills this agent can perform
        """
        self.agents[name] = {
            "name": name,
            "description": description,
            "capabilities": capabilities,
            "status": "active"
        }
        print(f"✅ Agent registered: {name}")
    
    def find_agent(self, capability: str):
        """
        Find an agent that has the required capability.
        Returns agent name if found, None otherwise.
        """
        for name, info in self.agents.items():
            if capability in info["capabilities"]:
                return name
        return None
    
    def list_agents(self):
        """Display all registered agents and their descriptions."""
        print("\n📋 Registered Agents:")
        for name, info in self.agents.items():
            print(f"  • {name}: {info['description']}")
        print()