# core/registry.py
# AgentOS - Agent Registry
# Manages registration and dynamic model selection for all agents

class AgentRegistry:
    """
    Central registry for all AgentOS agents.
    Agents register their capabilities AND supported models.
    The registry intelligently selects the best model for each task.
    This enables true Internet of Agents — agents choose their own LLM.
    """

    def __init__(self):
        self.agents = {}
        
        # Model performance profiles
        # Each model has strengths for different task types
        self.model_profiles = {
            "gemini-2.5-flash": {
                "provider": "Google",
                "strengths": ["research", "writing", "analysis", "multimodal"],
                "speed": "fast"
            },
            "glm-5.1": {
                "provider": "Zhipu AI",
                "strengths": ["strategic", "advise", "reasoning", "chinese"],
                "speed": "medium"
            },
            "deepseek-v4-pro": {
                "provider": "DeepSeek AI",
                "strengths": ["validate", "fact-check", "code", "critique"],
                "speed": "medium"
            }
        }

    def register(self, name: str, description: str, capabilities: list, supported_models: list = None):
        """
        Register a new agent with its capabilities and supported models.
        name: unique agent identifier
        description: what this agent does
        capabilities: list of skills this agent can perform
        supported_models: list of LLM models this agent can use
        """
        self.agents[name] = {
            "name": name,
            "description": description,
            "capabilities": capabilities,
            "supported_models": supported_models or ["gemini-2.5-flash"],
            "status": "active",
            "current_model": supported_models[0] if supported_models else "gemini-2.5-flash"
        }
        print(f"✅ Agent registered: {name} | Models: {supported_models or ['gemini-2.5-flash']}")

    def select_best_model(self, agent_name: str, task_type: str) -> str:
        """
        Dynamically select the best model for a given task.
        Matches task requirements with model strengths.
        This is the core of AgentOS intelligence — agents choose their own LLM!
        """
        agent = self.agents.get(agent_name)
        if not agent:
            return "gemini-2.5-flash"

        supported = agent["supported_models"]
        
        # Score each supported model based on task alignment
        best_model = supported[0]
        best_score = 0

        for model in supported:
            profile = self.model_profiles.get(model, {})
            strengths = profile.get("strengths", [])
            
            # Calculate match score
            score = sum(1 for s in strengths if s in task_type.lower())
            
            if score > best_score:
                best_score = score
                best_model = model

        # Update agent's current model
        self.agents[agent_name]["current_model"] = best_model
        provider = self.model_profiles.get(best_model, {}).get("provider", "Unknown")
        print(f"🧠 Model selected for {agent_name}: {best_model} ({provider})")
        
        return best_model

    def find_agent(self, capability: str):
        """Find an agent that has the required capability."""
        for name, info in self.agents.items():
            if capability in info["capabilities"]:
                return name
        return None

    def list_agents(self):
        """Display all registered agents with their models."""
        print("\n📋 Registered Agents:")
        for name, info in self.agents.items():
            models = ", ".join(info["supported_models"])
            print(f"  • {name}: {info['description']}")
            print(f"    └─ Models: {models}")
        print()