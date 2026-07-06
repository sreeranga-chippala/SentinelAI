"""
SentinelAI Mission Planner Wrapper Agent

Optimized Wrapper
- Reuses ADK Runner
- Reuses ADK Session
- Async-only (no asyncio.run())
"""

from __future__ import annotations

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.agents.mission_planner_agent import root_agent


class MissionPlannerAgent:

    def __init__(self):

        self.app_name = "SentinelAI"

        self.user_id = "planner_user"

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            app_name=self.app_name,
            agent=root_agent,
            session_service=self.session_service,
        )

        self.session = None

    async def _get_session(self):

        if self.session is None:

            self.session = await self.session_service.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
            )

        return self.session

    async def run_async(
        self,
        query: str,
    ) -> str:

        session = await self._get_session()

        message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=query,
                )
            ],
        )

        response = ""

        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session.id,
            new_message=message,
        ):

            if event.content is None:
                continue

            if event.content.parts is None:
                continue

            for part in event.content.parts:

                if getattr(part, "text", None):

                    response += part.text

        return response.strip()