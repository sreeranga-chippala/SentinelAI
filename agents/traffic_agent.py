"""
SentinelAI Traffic Wrapper Agent

Optimized Wrapper
- Reuses ADK Runner
- Reuses ADK Session
"""

from __future__ import annotations

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.agents.traffic_agent import root_agent


class TrafficAgent:

    def __init__(self):

        self.app_name = "SentinelAI"

        self.user_id = "traffic_user"

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
        origin: str,
        destination: str,
    ) -> str:

        session = await self._get_session()

        message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"""
Find the fastest rescue route
from {origin}
to {destination}.

Return:
- Best Route
- Distance
- Estimated Time
- Road Status
"""
                )
            ],
        )

        response = ""

        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session.id,
            new_message=message,
        ):

            if not event.content:
                continue

            if not event.content.parts:
                continue

            for part in event.content.parts:

                if getattr(part, "text", None):

                    response += part.text

        return response.strip()

    def run(
        self,
        origin: str,
        destination: str,
    ) -> str:

        import asyncio

        return asyncio.run(
            self.run_async(
                origin,
                destination,
            )
        )