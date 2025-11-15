# client_tool/agent.py

from google.adk.agents import Agent
from . import tools

root_agent = Agent(
    name="agent_orchestrator",
    model="gemini-2.0-flash",
    description="Orchestrates fact-checking + weather via A2A send_a2a_message",
    instruction="""
You are an orchestrator that answers user questions by delegating to two remote agents:

1. **check_fact** – verify any claim.
2. **get_weather** – get weather for a city.

**Steps:**

1. Read the query.
2. Call **check_fact** if a claim is present.
3. Call **get_weather** if a city is mentioned.
4. You may call both in parallel.
5. After tools return, read:
   - `tool_context.state["fact_result"]`
   - `tool_context.state["weather_result"]`
6. Combine into a clear answer.
7. If "debug" is in the query, show raw tool input/output.

End with: "Anything else?"
""",
    tools=[
        tools.check_fact,
        tools.get_weather,
    ],
)