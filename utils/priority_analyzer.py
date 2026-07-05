"""
utils/priority_analyzer.py

Combines all analysis results into a single priority assessment.

Input:
    AreaContext

Output:
    PriorityAssessment
"""

from models.area_context import AreaContext
from models.priority_assessment import PriorityAssessment


class PriorityAnalyzer:

    # ---------------------------------------------------------
    # Weight Configuration
    # ---------------------------------------------------------

    WEATHER_WEIGHT = 0.40
    POPULATION_WEIGHT = 0.30
    ROAD_WEIGHT = 0.15
    HOSPITAL_WEIGHT = 0.15

    # ---------------------------------------------------------

    @classmethod
    def analyze(cls, context: AreaContext) -> PriorityAssessment:

        weather_score = context.weather.risk_score

        population_score = context.population.vulnerability_score

        road_score = cls._calculate_route_score(
            context.nearby_routes
        )

        hospital_score = cls._calculate_hospital_score(
            context.nearby_hospitals
        )

        final_score = (

            weather_score * cls.WEATHER_WEIGHT +

            population_score * cls.POPULATION_WEIGHT +

            road_score * cls.ROAD_WEIGHT +

            hospital_score * cls.HOSPITAL_WEIGHT

        )

        final_score = round(final_score, 2)

        priority_level = cls._get_priority_level(
            final_score
        )

        action = cls._recommended_action(
            priority_level
        )

        reason = (
            f"Weather={weather_score}, "
            f"Population={population_score}, "
            f"Road={road_score}, "
            f"Hospital={hospital_score}"
        )

        return PriorityAssessment(

            area_id=context.area_id,

            area_name=context.area_name,

            priority_score=final_score,

            priority_level=priority_level,

            reason=reason,

            recommended_action=action

        )

    # ---------------------------------------------------------

    @staticmethod
    def _calculate_route_score(routes):

        """
        Returns a score between 0 and 100.

        Higher means roads are worse.
        """

        if not routes:
            return 100

        blocked = sum(
            1
            for route in routes
            if route.route_status == "Blocked"
        )

        unsafe = sum(
            1
            for route in routes
            if route.route_status == "Unsafe"
        )

        total = len(routes)

        score = (
            (blocked * 100) +
            (unsafe * 60)
        ) / total

        return min(round(score), 100)

    # ---------------------------------------------------------

    @staticmethod
    def _calculate_hospital_score(hospitals):

        """
        Returns a score between 0 and 100.

        Higher means hospitals are under pressure.
        """

        if not hospitals:
            return 100

        occupancy = sum(
            h.occupancy_percentage
            for h in hospitals
        )

        average = occupancy / len(hospitals)

        return round(average)

    # ---------------------------------------------------------

    @staticmethod
    def _get_priority_level(score):

        if score >= 85:
            return "Extreme"

        elif score >= 70:
            return "Critical"

        elif score >= 55:
            return "High"

        elif score >= 35:
            return "Medium"

        return "Low"

    # ---------------------------------------------------------

    @staticmethod
    def _recommended_action(level):

        actions = {

            "Extreme":
                "Immediate evacuation and maximum resource deployment",

            "Critical":
                "Deploy rescue teams and medical support",

            "High":
                "Prepare evacuation and mobilize resources",

            "Medium":
                "Continuous monitoring and standby teams",

            "Low":
                "Routine monitoring"

        }

        return actions[level]