# core/message_bus.py
# AgentOS - Message Bus
# Handles communication between agents without direct coupling

from datetime import datetime

class MessageBus:
    """
    Central message bus for inter-agent communication.
    Agents can publish messages and subscribe to receive them.
    This enables agents to collaborate without knowing each other directly.
    """

    def __init__(self):
        # Stores all messages exchanged between agents
        self.messages = []
        # Stores task results from each agent
        self.results = {}

    def publish(self, sender: str, receiver: str, content: str, task_id: str):
        """
        Publish a message from one agent to another.
        sender: name of the agent sending the message
        receiver: name of the agent receiving the message
        content: the actual message or task description
        task_id: unique identifier for tracking the task
        """
        message = {
            "task_id": task_id,
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        self.messages.append(message)
        print(f"📨 Message sent: {sender} → {receiver}")
        return message

    def store_result(self, agent_name: str, task_id: str, result: str):
        """
        Store the output result from an agent after completing a task.
        agent_name: which agent produced this result
        task_id: which task this result belongs to
        result: the actual output content
        """
        if task_id not in self.results:
            self.results[task_id] = {}
        
        self.results[task_id][agent_name] = {
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        print(f"✅ Result stored from: {agent_name}")

    def get_results(self, task_id: str):
        """
        Retrieve all results for a specific task.
        Returns combined outputs from all agents.
        """
        return self.results.get(task_id, {})

    def get_history(self):
        """Return full message history for audit and transparency."""
        return self.messages