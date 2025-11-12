# client_subagent/agent.py

from google.adk.agents import Agent   
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# sub agent
fact_agent = RemoteA2aAgent(
    name="fact_checker",
    description="Agent to give check facts",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
    timeout=300.0,
)

# sub agent
weather_agent = RemoteA2aAgent(
    name="weather_checker",
    description="Agent to give weather information",
    agent_card="http://localhost:8002/.well-known/agent-card.json",
    timeout=300.0,
)

# orchestrator agent 
root_agent = Agent(
    name="agent_orchestrator",
    model="gemini-2.5-flash",
    description="Gets facts from multiple remote agents",
    sub_agents=[fact_agent, weather_agent], 
)