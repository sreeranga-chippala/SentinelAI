"""
models/road.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Road:

    road_id: str

    road_name: str

    area_id: str

    start_area: str

    end_area: str

    traffic_level: str

    water_level: float

    is_blocked: bool

    travel_time: int