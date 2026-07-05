"""
utils/communication_engine.py
"""

from uuid import uuid4
from datetime import datetime

from models.public_alert import PublicAlert


class CommunicationEngine:

    @staticmethod
    def create_alert(mission):

        title = f"{mission.priority_level} Emergency"

        message = (
            f"Emergency response initiated for {mission.area_name}. "
            f"{mission.rescue_teams} rescue teams, "
            f"{mission.boats} boats, "
            f"{mission.ambulances} ambulances have been deployed. "
            f"Nearest hospital: {mission.assigned_hospital}."
        )

        return PublicAlert(

            alert_id=str(uuid4()),

            area_id=mission.area_id,

            area_name=mission.area_name,

            priority_level=mission.priority_level,

            title=title,

            message=message,

            issued_at=datetime.now(),

            target="PUBLIC",

            status="READY"
        )