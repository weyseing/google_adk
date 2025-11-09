# remote_a2a/facts_agent/agent.py

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# tools
async def get_fact(topic: str) -> str:
    """Provides interesting facts about a topic.
    Args:
        topic: The topic to get facts about (e.g., 'python', 'space', 'ai')
    """
    facts_db = {
        "python": "Python was created by Guido van Rossum and released in 1991.",
        "space": "The ISS travels at 28,000 km/h, orbiting Earth every 90 minutes.",
        "ai": "The first AI program was written in 1951 by Christopher Strachey."
    }
    return facts_db.get(topic.lower(), f"I don't have facts about '{topic}' yet.")

# agent
root_agent = Agent(
    name="facts_agent",
    model="gemini-2.0-flash",
    description="A helpful agent that provides facts about various topics.",
    tools=[get_fact],
    instruction="""You are a factual knowledge agent. 
    When asked about a topic, use the get_fact tool to provide accurate information.
    If no fact is available, suggest similar topics you know about."""
)

# a2a app
a2a_app = to_a2a(root_agent, port=8001)
