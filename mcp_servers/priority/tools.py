"""
Priority MCP Tools
------------------
Calculates disaster response priority based on incident parameters.
"""

from typing import Dict


class PriorityToolException(Exception):
    """Raised when priority calculation fails."""
    pass


WEATHER_SCORE = {
    "clear": 0,
    "clouds": 2,
    "rain": 5,
    "heavy rain": 8,
    "thunderstorm": 10,
    "storm": 10,
    "fog": 4,
    "mist": 2,
    "snow": 6,
}


ROAD_SCORE = {
    "good": 0,
    "moderate": 4,
    "difficult": 7,
    "blocked": 10,
}


def _normalize_weather(weather: str) -> str:
    return weather.strip().lower()


def _normalize_road(status: str) -> str:
    return status.strip().lower()


async def calculate_priority(
    severity: int,
    affected_people: int,
    critical_injuries: int,
    distance_km: float,
    weather: str,
    road_access: str,
) -> Dict:
    """
    Calculates a disaster response priority score.

    Parameters
    ----------
    severity : 1-10
    affected_people : int
    critical_injuries : int
    distance_km : float
    weather : str
    road_access : str
    """

    try:

        severity = max(1, min(10, severity))
        affected_people = max(0, affected_people)
        critical_injuries = max(0, critical_injuries)
        distance_km = max(0.0, distance_km)

        # -----------------------------
        # Severity (40)
        # -----------------------------
        severity_score = (severity / 10) * 40

        # -----------------------------
        # Injuries (25)
        # -----------------------------
        injury_score = min(critical_injuries, 100) / 100 * 25

        # -----------------------------
        # Population (15)
        # -----------------------------
        people_score = min(affected_people, 1000) / 1000 * 15

        # -----------------------------
        # Distance (10)
        # Closer incidents deserve faster response
        # -----------------------------
        if distance_km <= 5:
            distance_score = 10
        elif distance_km <= 15:
            distance_score = 8
        elif distance_km <= 30:
            distance_score = 6
        elif distance_km <= 60:
            distance_score = 4
        else:
            distance_score = 2

        # -----------------------------
        # Weather (5)
        # -----------------------------
        weather_score = (
            WEATHER_SCORE.get(_normalize_weather(weather), 2) / 10
        ) * 5

        # -----------------------------
        # Road Access (5)
        # -----------------------------
        road_score = (
            ROAD_SCORE.get(_normalize_road(road_access), 4) / 10
        ) * 5

        total = round(
            severity_score
            + injury_score
            + people_score
            + distance_score
            + weather_score
            + road_score
        )

        total = max(0, min(100, total))

        if total >= 90:
            level = "CRITICAL"
            recommendation = (
                "Immediate dispatch of all available emergency resources."
            )

        elif total >= 70:
            level = "HIGH"
            recommendation = (
                "High priority. Dispatch emergency response immediately."
            )

        elif total >= 40:
            level = "MEDIUM"
            recommendation = (
                "Monitor continuously and dispatch resources as available."
            )

        else:
            level = "LOW"
            recommendation = (
                "Routine response is sufficient."
            )

        return {
            "success": True,
            "priority_score": total,
            "priority_level": level,
            "recommendation": recommendation,
            "factors": {
                "severity": severity,
                "affected_people": affected_people,
                "critical_injuries": critical_injuries,
                "distance_km": distance_km,
                "weather": weather,
                "road_access": road_access,
            },
        }

    except Exception as exc:
        raise PriorityToolException(str(exc))