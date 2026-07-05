"""
models/population_assessment.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class PopulationAssessment:

    area_id: str

    area_name: str

    total_population: int

    children: int

    adults: int

    elderly: int

    disabled: int

    rescue_requests: int

    vulnerability_score: int

    priority_level: str

    reason: str