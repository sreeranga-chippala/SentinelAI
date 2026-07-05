"""
agents/hospital_agent.py

Hospital Agent

Responsibilities
----------------
1. Fetch hospital information from HospitalServer.
2. Analyze each hospital.
3. Group HospitalStatus by area.
4. Return the analysis results.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent
from utils.hospital_analyzer import HospitalAnalyzer


class HospitalAgent(BaseAgent):

    def __init__(
        self,
        hospital_server,
        logger=None
    ):

        super().__init__(logger)

        self.hospital_server = hospital_server

    # ----------------------------------------------------------

    def run(self):

        self.before_run()

        hospitals = self.hospital_server.get_all_hospitals()

        results = {}

        for area_id, hospital_list in hospitals.items():

            area_status = []

            for hospital in hospital_list:

                status = HospitalAnalyzer.analyze(hospital)

                area_status.append(status)

                self.log(
                    f"{hospital.name} -> "
                    f"{status.status} "
                    f"({status.available_beds}/{status.total_beds} beds)"
                )

            results[area_id] = area_status

        self.after_run()

        return results