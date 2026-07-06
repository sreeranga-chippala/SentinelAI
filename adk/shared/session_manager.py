"""
adk/sessions/session_manager.py

Creates and manages ADK sessions.
"""

from google.adk.sessions import InMemorySessionService

from adk.shared.config import Config


class SessionManager:

    def __init__(self):

        self.service = InMemorySessionService()

        self._created = False

    async def create(self):

        if self._created:
            return

        await self.service.create_session(

            app_name=Config.APP_NAME,

            user_id=Config.USER_ID,

            session_id=Config.SESSION_ID

        )

        self._created = True

    def get_service(self):

        return self.service