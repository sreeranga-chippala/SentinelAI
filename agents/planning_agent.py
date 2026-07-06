"""
SentinelAI Planning Wrapper Agent

Wrapper around the Google ADK Planning Agent.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.agents.planning_agent import root_agent


class PlanningAgent:
    """
    Wrapper for the ADK Planning Agent.
    """

    def __init__(self) -> None:

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            app_name="SentinelAI",
            agent=root_agent,
            session_service=self.session_service,
        )

    async def run_async(
        self,
        query: str,
    ) -> str:

        session = await self.session_service.create_session(
            app_name="SentinelAI",
            user_id="planning_user",
        )

        message = types.Content(
            role="user",
            parts=[
                types.Part(text=query),
            ],
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id="planning_user",
            session_id=session.id,
            new_message=message,
        ):

            if event.content and event.content.parts:

                for part in event.content.parts:

                    if getattr(part, "text", None):

                        final_response += part.text

        return final_response.strip()

    def run(
        self,
        query: str,
    ) -> str:

        return asyncio.run(
            self.run_async(query)
        )