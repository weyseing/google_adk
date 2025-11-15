# client_tool/tools.py

from google.adk.tools.tool_context import ToolContext
from .a2a_client import CustomA2AClient

# Remote clients
fact_client = CustomA2AClient(
    name="fact_checker",
    base_url="http://localhost:8001",
    required_extensions={},
)

weather_client = CustomA2AClient(
    name="weather_checker",
    base_url="http://localhost:8002",
    required_extensions={},
)

# check fact
async def check_fact(statement: str, tool_context: ToolContext) -> str:
    message = fact_client.create_message(statement)
    task = await fact_client.send_a2a_message(message)

    texts = [
        part.root.text
        for artifact in task.artifacts
        for part in artifact.parts
        if hasattr(part.root, "text")
    ]
    result = "\n".join(texts) if texts else "No response"

    tool_context.state["fact_result"] = result
    return result

# check weather
async def get_weather(city: str, tool_context: ToolContext) -> str:
    query = f"Weather in {city}"
    message = weather_client.create_message(query)
    task = await weather_client.send_a2a_message(message)

    texts = [
        part.root.text
        for artifact in task.artifacts
        for part in artifact.parts
        if hasattr(part.root, "text")
    ]
    result = "\n".join(texts) if texts else "No weather data"

    tool_context.state["weather_result"] = result
    return result