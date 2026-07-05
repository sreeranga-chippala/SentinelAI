"""
models/resource.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Resource:

    rescue_teams: int

    boats: int

    ambulances: int

    helicopters: int

    food_packets: int

    medical_kits: int