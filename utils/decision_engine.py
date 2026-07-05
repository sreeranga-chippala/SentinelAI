"""
utils/decision_engine.py
"""

from uuid import uuid4
from datetime import datetime

from models.mission import Mission


class DecisionEngine:

    @staticmethod
    def create_mission(priority, allocation):

        return Mission(

            mission_id=str(uuid4()),

            area_id=priority.area_id,

            area_name=priority.area_name,

            priority_level=priority.priority_level,

            assigned_hospital=allocation.assigned_hospital,

            rescue_teams=allocation.rescue_teams,

            boats=allocation.boats,

            ambulances=allocation.ambulances,

            helicopters=allocation.helicopters,

            food_packets=allocation.food_packets,

            medical_kits=allocation.medical_kits,

            status="READY",

            created_at=datetime.now(),

            remarks=allocation.message

        )