"""
agents/priority_agent.py

Priority Agent

Responsibilities
----------------
1. Read analysis results.
2. Build AreaContext for each area.
3. Generate PriorityAssessment.
4. Return the priority assessments.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent

from models.area_context import AreaContext

from utils.priority_analyzer import PriorityAnalyzer


class PriorityAgent(BaseAgent):

    def __init__(self, logger=None):

        super().__init__(logger)

    # ----------------------------------------------------------

    def run(
        self,
        weather_results,
        population_results,
        hospital_results,
        route_results
    ):

        self.before_run()

        priorities = {}

        area_ids = weather_results.keys()

        for area_id in area_ids:

            weather = weather_results.get(area_id)

            population = population_results.get(area_id)

            hospitals = hospital_results.get(area_id, [])

            routes = route_results.get(area_id, [])

            if weather is None or population is None:

                self.log(
                    f"Skipping {area_id}: Missing analysis data."
                )

                continue

            context = AreaContext(

                area_id=area_id,

                area_name=weather.area_name,

                weather=weather,

                population=population,

                nearby_routes=routes,

                nearby_hospitals=hospitals

            )

            assessment = PriorityAnalyzer.analyze(context)

            priorities[area_id] = assessment

            self.log(
                f"{assessment.area_name} -> "
                f"{assessment.priority_level} "
                f"(Score={assessment.priority_score})"
            )

        self.after_run()

        return priorities