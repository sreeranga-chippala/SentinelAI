"""
Session Manager
"""

from google.adk.sessions import InMemorySessionService

from adk.shared.config import Config


class SessionManager:

    def __init__(self):

        self.service = InMemorySessionService()

        self.created = False

    async def initialize(self):

        if self.created:
            return

        await self.service.create_session(

            app_name=Config.APP_NAME,

            user_id=Config.USER_ID,

            session_id=Config.SESSION_ID

        )

        self.created = True