"""
agents/population_agent.py

Population Agent

Responsibilities
----------------
1. Fetch population information from PopulationServer.
2. Analyze population vulnerability for each area.
3. Return PopulationAssessment objects.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent
from utils.population_analyzer import PopulationAnalyzer


class PopulationAgent(BaseAgent):

    def __init__(
        self,
        population_server,
        logger=None
    ):

        super().__init__(logger)

        self.population_server = population_server

    # ----------------------------------------------------------

    def run(self):

        self.before_run()

        areas = self.population_server.get_all_population()

        results = {}

        for area_id, area in areas.items():

            assessment = PopulationAnalyzer.analyze(area)

            results[area_id] = assessment

            self.log(
                f"{area.name} -> "
                f"{assessment.priority_level} "
                f"(Score={assessment.vulnerability_score})"
            )

        self.after_run()

        return results