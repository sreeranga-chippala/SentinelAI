"""
SentinelAI Weather Wrapper Agent

Coordinator interacts only with this wrapper.
"""

from __future__ import annotations

import asyncio
from uuid import uuid4

from google.genai import types

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from adk.agents.weather_agent import root_agent


class WeatherAgent:
    """
    Wrapper around the Google ADK Weather Agent.
    """

    def __init__(self) -> None:

        self.app_name = "SentinelAI"

        self.user_id = "system"

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            agent=root_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )

    async def run_async(
        self,
        query: str,
    ) -> str:

        session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=str(uuid4()),
        )

        message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=query,
                )
            ],
        )

        final_response = ""

        async for event in self.runner.run_async(
            session_id=session.id,
            user_id=self.user_id,
            new_message=message,
        ):

            if event.content is None:
                continue

            if event.content.parts is None:
                continue

            for part in event.content.parts:

                if getattr(part, "text", None):

                    final_response += part.text

        return final_response.strip()

    def run(
        self,
        query: str,
    ) -> str:

        return asyncio.run(
            self.run_async(
                query,
            )
        )