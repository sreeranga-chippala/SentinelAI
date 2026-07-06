"""
adk/runners/runner.py

Creates ADK runners.
"""

from google.adk.runners import Runner

from adk.shared.config import Config


class RunnerFactory:

    @staticmethod
    def create(agent, session_service):

        return Runner(

            agent=agent,

            app_name=Config.APP_NAME,

            session_service=session_service

        )