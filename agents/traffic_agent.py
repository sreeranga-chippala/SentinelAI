"""
SentinelAI - Traffic Wrapper Agent

Wrapper around the Google ADK Traffic Agent.
"""

from __future__ import annotations
from google.genai import types
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from adk.agents.traffic_agent import root_agent


class TrafficAgent:
    """
    Wrapper for the ADK Traffic Agent.
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
        Execute the Traffic ADK agent.
        """

        session = await self.session_service.create_session(
            app_name="SentinelAI",
            user_id="traffic_user",
        )

        final_response = ""

        message = types.Content(
            role="user",
            parts=[
                types.Part(text=query),
            ],
        )

        async for event in self.runner.run_async(
            user_id="traffic_user",
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
            self.run_async(query)
        )