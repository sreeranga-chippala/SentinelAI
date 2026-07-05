"""
models/allocation_plan.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class AllocationPlan:

    area_id: str

    area_name: str

    assigned_hospital: str

    beds_allocated: int

    rescue_teams: int

    boats: int

    ambulances: int

    helicopters: int

    food_packets: int

    medical_kits: int

    success: bool

    message: str