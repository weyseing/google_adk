# client_tool/agent.py

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools import AgentTool  # Correct import for agent-as-tool

# Remote A2A agents (these become tools via AgentTool)
fact_remote = RemoteA2aAgent(
    name="fact_checker",
    description="Remote agent to check facts",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
    timeout=300.0,
)

weather_remote = RemoteA2aAgent(
    name="weather_checker",
    description="Remote agent to get weather information",
    agent_card="http://localhost:8002/.well-known/agent-card.json",
    timeout=300.0,
)

# Wrap remotes as tools (AgentTool handles invocation schema automatically)
fact_tool = AgentTool(agent=fact_remote)
weather_tool = AgentTool(agent=weather_remote)

# Root orchestrator agent
root_agent = Agent(
    name="agent_orchestrator",
    model="gemini-2.0-flash",  # Use a valid model; adjust if needed
    description="Orchestrates fact-checking and weather queries using remote A2A tools",
    tools=[fact_tool, weather_tool],  # Pass tool instances here
)