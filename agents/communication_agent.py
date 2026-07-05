"""
agents/communication_agent.py

Communication Agent

Responsibilities
----------------
1. Receive Mission objects.
2. Generate PublicAlert objects.
3. Send alerts using NotificationServer.
4. Return PublicAlert objects.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent

from utils.communication_engine import CommunicationEngine


class CommunicationAgent(BaseAgent):

    def __init__(
        self,
        notification_server,
        logger=None
    ):

        super().__init__(logger)

        self.notification_server = notification_server

    # ----------------------------------------------------------

    def run(
        self,
        mission_results
    ):

        self.before_run()

        alert_results = {}

        for area_id, mission in mission_results.items():

            alert = CommunicationEngine.create_alert(
                mission
            )

            success = self.notification_server.send_alert(
                alert
            )

            if success:

                alert.status = "SENT"

            else:

                alert.status = "FAILED"

            alert_results[area_id] = alert

            self.log(

                f"{mission.area_name} -> "

                f"{alert.status}"

            )

        self.after_run()

        return alert_results