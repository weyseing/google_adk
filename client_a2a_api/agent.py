# client_a2a_api/agent.py
from google.adk import Agent

def get_fact(query: str) -> str:
    """Provide interesting facts about various topics."""
    facts = {
        "space": "A day on Venus is longer than its year.",
        "ocean": "The ocean covers 71% of Earth's surface.",
        "technology": "The first computer bug was an actual moth found in 1947.",
        "history": "The shortest war in history lasted 38 minutes (Anglo-Zanzibar War).",
        "default": "Honey never spoils. Archaeologists have found 3,000-year-old honey."
    }
    return facts.get(query.lower(), facts["default"])

root_agent = Agent(
    name="fact_agent",
    model="gemini-2.0-flash",
    description="Agent to give interesting facts.",
    instruction="Provide interesting facts when asked. Use the get_fact tool.",
    tools=[get_fact]
)