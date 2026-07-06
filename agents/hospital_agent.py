"""
SentinelAI Hospital Wrapper Agent

Optimized Wrapper
- Reuses ADK Runner
- Reuses ADK Session
- Handles MCP failures gracefully
"""

from __future__ import annotations

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from adk.agents.hospital_agent import root_agent


class HospitalAgent:

    def __init__(self):

        self.app_name = "SentinelAI"

        self.user_id = "hospital_user"

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
        location: str,
    ) -> str:

        session = await self._get_session()

        message = types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"""
Find nearby hospitals in {location}.

Return only

- Hospital Name
- Emergency Facility
- Phone Number
- Coordinates
"""
                )
            ],
        )

        response = ""

        try:

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

        except Exception as exc:

            return f"ERROR: Hospital MCP failed ({exc})"

        response = response.strip()

        if not response:

            return "ERROR: Hospital MCP returned an empty response."

        lower = response.lower()

        failure_keywords = (
            "i am sorry",
            "unable",
            "unavailable",
            "cannot",
            "can't",
            "failed",
            "failure",
            "timeout",
            "timed out",
            "error",
            "internal server",
            "service unavailable",
        )

        if any(keyword in lower for keyword in failure_keywords):

            return (
                "ERROR: Hospital service is temporarily unavailable. "
                "Unable to retrieve nearby hospitals."
            )

        return response

    def run(
        self,
        location: str,
    ) -> str:

        return asyncio.run(
            self.run_async(location)
        )