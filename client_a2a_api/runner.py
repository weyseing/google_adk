# client_a2a_api/runner.py
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from .agent import root_agent

APP_NAME = "fact_app"
USER_ID = "user_1"
SESSION_ID = "session_1"

async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    content = types.Content(role="user", parts=[types.Part(text="tell me a fact about space")])
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            print("Response:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
