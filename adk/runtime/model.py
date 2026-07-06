"""
Loads Gemini model configuration.
"""

from google.genai import Client

from adk.shared.config import Config


class ModelManager:

    _client = None

    @classmethod
    def client(cls):

        if cls._client is None:

            cls._client = Client(
                api_key=Config.GEMINI_API_KEY
            )

        return cls._client

    @classmethod
    def model(cls):

        return Config.MODEL