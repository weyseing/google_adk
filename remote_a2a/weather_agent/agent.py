# remote_a2a/weather_agent/agent.py

from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# tool
async def get_weather(city: str) -> str:
    """Get current weather for a city.
    Args:
        city: City name (e.g., 'London', 'Tokyo', 'New York')
    """
    weather_db = {
        "london": "🌧️ 12°C, cloudy with light rain. Winds 15 km/h.",
        "tokyo": "☀️ 22°C, clear and sunny. Humidity 45%.",
        "new york": "⛅ 18°C, partly cloudy. Winds 10 km/h.",
        "paris": "🌤️ 16°C, mostly sunny. Light breeze.",
        "singapore": "🌤️ 30°C, hot and humid. Occasional showers.",
    }
    
    return weather_db.get(
        city.lower(), 
        f"❌ Weather data for '{city}' not available. Try: London, Tokyo, New York, Paris, or Singapore."
    )

# agent
root_agent = Agent(
    name="weather_sub_agent",
    model="gemini-2.5-flash",
    description="A sub-agent that provides current weather information for major cities.",
    tools=[get_weather],
    instruction="""You are a weather information specialist. 
    When asked about weather, always use the get_weather tool.
    If the city is not found, suggest the available cities."""
)

# a2a app
a2a_app = to_a2a(root_agent, port=8002)