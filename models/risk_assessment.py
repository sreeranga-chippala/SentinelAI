"""
models/risk_assessment.py

Represents the result of weather risk analysis.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RiskAssessment:

    area_id: str

    area_name: str

    rainfall: float

    river_level: float

    humidity: float

    forecast: str

    risk_level: str

    risk_score: int

    reason: str