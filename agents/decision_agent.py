"""
SentinelAI Decision Agent Wrapper
"""

import asyncio

from google.genai.types import Content
from google.genai.types import Part

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from adk.agents.decision_agent import root_agent


class DecisionAgent:

    def __init__(self):

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            app_name="decision_app",
            agent=root_agent,
            session_service=self.session_service,
        )

    async def run_async(self, query: str) -> str:

        session = await self.session_service.create_session(
            app_name="decision_app",
            user_id="user",
        )

        message = Content(
            role="user",
            parts=[
                Part(text=query),
            ],
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id="user",
            session_id=session.id,
            new_message=message,
        ):

            if event.content:

                for part in event.content.parts:

                    if getattr(part, "text", None):
                        final_response += part.text

        return final_response.strip()

    def run(self, query: str) -> str:

        return asyncio.run(
            self.run_async(query)
        )