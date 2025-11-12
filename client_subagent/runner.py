# client_subagent/runner.py
import time
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agent import root_agent

# app name, user id
APP_NAME = "fact_app"
USER_ID = "user_1"

async def main():
    # session service
    session_id = f"{USER_ID}_{int(time.time())}"
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    # runner
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # question
    content = types.Content(role="user", parts=[types.Part(text="tell me a fact about java")])
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=content):
        if event.is_final_response():
            print("Response:", event.content.parts[0].text)

    # history question
    content = types.Content(role="user", parts=[types.Part(text="what is my previoys question?")])
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=content):
        if event.is_final_response():
            print("Response:", event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
