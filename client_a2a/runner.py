# client_a2a/runner.py
import asyncio
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agent import root_agent

# app name, user id, session id
APP_NAME = "fact_app"
USER_ID = "user_1"
SESSION_ID = "session_1"

async def main():
    # session service
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # runner
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # message
    content = types.Content(role="user", parts=[types.Part(text="tell me a fact about java")])

    # async run
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Response:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
