"""
agents/traffic_agent.py

Traffic Agent

Responsibilities
----------------
1. Fetch road information from TrafficServer.
2. Analyze every road.
3. Group RouteAssessment by area.
4. Return the analysis results.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent
from utils.traffic_analyzer import TrafficAnalyzer


class TrafficAgent(BaseAgent):

    def __init__(
        self,
        traffic_server,
        logger=None
    ):

        super().__init__(logger)

        self.traffic_server = traffic_server

    # ----------------------------------------------------------

    def run(self):

        self.before_run()

        roads = self.traffic_server.get_all_roads()

        results = {}

        for area_id, road_list in roads.items():

            area_routes = []

            for road in road_list:

                assessment = TrafficAnalyzer.analyze(road)

                area_routes.append(assessment)

                self.log(
                    f"{road.road_name} -> "
                    f"{assessment.route_status} "
                    f"(Travel Time: {assessment.travel_time} mins)"
                )

            results[area_id] = area_routes

        self.after_run()

        return results