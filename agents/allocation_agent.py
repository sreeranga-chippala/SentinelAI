"""
SentinelAI - Allocation Wrapper Agent

Wrapper around the Google ADK Allocation Agent.
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.agents.allocation_agent import root_agent


class AllocationAgent:
    """
    Wrapper for the ADK Allocation Agent.
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
        """
        Execute the Allocation ADK agent.
        """

        session = await self.session_service.create_session(
            app_name="SentinelAI",
            user_id="allocation_user",
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
            user_id="allocation_user",
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
        """
        Synchronous wrapper.
        """

        return asyncio.run(
            self.run_async(
                query,
            )
        )