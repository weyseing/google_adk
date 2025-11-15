# client_local_subagent/agent.py

from google.adk.agents import Agent   
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# import sub agent
from remote_a2a.facts_agent.agent import root_agent as fact_agent
from remote_a2a.weather_agent.agent import root_agent as weather_agent

# orchestrator agent 
root_agent = Agent(
    name="agent_orchestrator",
    model="gemini-2.0-flash",
    description="Gets facts from multiple remote agents",
    sub_agents=[fact_agent, weather_agent], 
)