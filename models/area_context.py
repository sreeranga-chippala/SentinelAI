"""
models/area_context.py

Represents the complete operational context of an area.

The AreaContext aggregates outputs from all analysis agents
(Weather, Population, Traffic, Hospital) into a single object
that planning agents (Priority, Allocation, Decision) can use.

Author: SentinelAI
"""

from dataclasses import dataclass, field

from models.risk_assessment import RiskAssessment
from models.population_assessment import PopulationAssessment
from models.route_assessment import RouteAssessment
from models.hospital_status import HospitalStatus


@dataclass(slots=True)
class AreaContext:
    """
    Represents everything SentinelAI knows about one area.

    Example
    -------
    RR Nagar

        Weather
        Population
        Nearby Roads
        Nearby Hospitals

    ↓

    PriorityAgent
    """

    # -----------------------------------------------------
    # Area Information
    # -----------------------------------------------------

    area_id: str

    area_name: str

    # -----------------------------------------------------
    # Analysis Results
    # -----------------------------------------------------

    weather: RiskAssessment

    population: PopulationAssessment

    nearby_routes: list[RouteAssessment] = field(default_factory=list)

    nearby_hospitals: list[HospitalStatus] = field(default_factory=list)