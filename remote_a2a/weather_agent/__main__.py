# remote_a2a/weather_agent/__main__.py

import sys
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from .agent import root_agent

if __name__ == "__main__":
    # hot reload
    reload = "--reload" in sys.argv

    # uvicorn server
    uvicorn.run(
        "remote_a2a.weather_agent.agent:a2a_app", 
        host="0.0.0.0",
        port=8002,
        reload=reload,  
        log_level="info"
    )