"""
utils/traffic_analyzer.py

Contains road accessibility analysis logic.
"""

from models.route_assessment import RouteAssessment


class TrafficAnalyzer:

    @staticmethod
    def analyze(road):

        score = 100
        reasons = []

        # ---------------- Water Level ----------------

        if road.water_level >= 1.5:
            score -= 60
            reasons.append("Severe waterlogging")

        elif road.water_level >= 1.0:
            score -= 40
            reasons.append("Heavy waterlogging")

        elif road.water_level >= 0.5:
            score -= 20
            reasons.append("Moderate waterlogging")

        # ---------------- Traffic ----------------

        if road.traffic_level == "High":
            score -= 20
            reasons.append("Heavy traffic")

        elif road.traffic_level == "Medium":
            score -= 10
            reasons.append("Moderate traffic")

        # ---------------- Blocked ----------------

        if road.is_blocked:
            score = 0
            reasons.append("Road blocked")

        # ---------------- Final Status ----------------

        if score == 0:
            status = "Blocked"

        elif score >= 80:
            status = "Safe"

        elif score >= 50:
            status = "Slow"

        else:
            status = "Unsafe"

        return RouteAssessment(
            road_id=road.road_id,
            road_name=road.road_name,
            start_area=road.start_area,
            end_area=road.end_area,
            traffic_level=road.traffic_level,
            water_level=road.water_level,
            is_blocked=road.is_blocked,
            travel_time=road.travel_time,
            safety_score=score,
            route_status=status,
            reason=", ".join(reasons)
        )