"""
agents/weather_agent.py

Weather Agent

Responsibilities
----------------
1. Fetch weather data from WeatherServer.
2. Analyze weather for each area.
3. Return RiskAssessment objects.

NOTE:
This agent NEVER modifies WorldState.
Coordinator is responsible for committing results.
"""

from agents.base_agent import BaseAgent
from utils.weather_analyzer import WeatherAnalyzer


class WeatherAgent(BaseAgent):

    def __init__(
        self,
        weather_server,
        logger=None
    ):

        super().__init__(logger)

        self.weather_server = weather_server

    # ----------------------------------------------------------

    def run(self):

        self.before_run()

        weather_data = self.weather_server.get_all_weather()

        assessments = {}

        for area_id, weather in weather_data.items():

            assessment = WeatherAnalyzer.analyze(

                area=weather["area"],

                rainfall=weather["rainfall"],

                river_level=weather["river_level"],

                humidity=weather["humidity"],

                forecast=weather["forecast"]

            )

            assessments[area_id] = assessment

            self.log(

                f"{weather['area']} -> "
                f"{assessment.risk_level} "
                f"(Score={assessment.risk_score})"

            )

        self.after_run()

        return assessments