"""
adk/shared/models.py

Shared request / response models for ADK agents.
"""

from pydantic import BaseModel


class AgentResponse(BaseModel):

    success: bool

    message: str

    data: dict