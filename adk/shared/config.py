"""
adk/shared/config.py

Global configuration for SentinelAI ADK.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    MODEL = "gemini-2.5-flash"

    APP_NAME = "SentinelAI"

    USER_ID = "commander"

    SESSION_ID = "sentinel-session"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not found in .env"
        )