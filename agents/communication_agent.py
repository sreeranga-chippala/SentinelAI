"""
Communication Agent Wrapper
"""

import asyncio

from google.genai.types import Content
from google.genai.types import Part

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from adk.agents.communication_agent import root_agent


class CommunicationAgent:

    def __init__(self):

        self.runner = Runner(
            app_name="communication_agent",
            agent=root_agent,
            session_service=InMemorySessionService(),
        )

    async def run_async(self, query: str):

        session = await self.runner.session_service.create_session(
            app_name="communication_agent",
            user_id="user",
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id="user",
            session_id=session.id,
            new_message=Content(
                role="user",
                parts=[Part(text=query)],
            ),
        ):

            if event.content:

                for part in event.content.parts:

                    if hasattr(part, "text") and part.text:
                        final_response += part.text

        return final_response

    def run(self, query: str):

        return asyncio.run(
            self.run_async(query)
        )