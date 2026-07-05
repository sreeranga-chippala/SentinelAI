"""
models/route_assessment.py

Represents the accessibility and safety status of a road.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RouteAssessment:

    road_id: str

    road_name: str

    start_area: str

    end_area: str

    traffic_level: str

    water_level: float

    is_blocked: bool

    travel_time: int

    safety_score: int

    route_status: str

    reason: str