"""
models/hospital_status.py
"""

from dataclasses import dataclass


@dataclass(slots=True)
class HospitalStatus:

    hospital_id: str

    name: str

    total_beds: int

    available_beds: int

    occupied_beds: int

    occupancy_percentage: float

    icu_beds: int

    emergency_capacity: int

    status: str