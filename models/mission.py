"""
models/mission.py
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Mission:

    mission_id: str

    area_id: str

    area_name: str

    priority_level: str

    assigned_hospital: str

    rescue_teams: int

    boats: int

    ambulances: int

    helicopters: int

    food_packets: int

    medical_kits: int

    status: str

    created_at: datetime

    remarks: str