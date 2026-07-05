"""
utils/weather_analyzer.py

Contains flood risk analysis logic.
"""

from models.risk_assessment import RiskAssessment


class WeatherAnalyzer:

    @staticmethod
    def analyze(
        area_id: str,
        area_name: str,
        rainfall: float,
        river_level: float,
        humidity: float,
        forecast: str,
    ) -> RiskAssessment:

        score = 0

        reasons = []

        # ----------------------------------------------------
        # Rainfall
        # ----------------------------------------------------

        if rainfall >= 250:

            score += 40

            reasons.append("Extreme rainfall")

        elif rainfall >= 180:

            score += 30

            reasons.append("Heavy rainfall")

        elif rainfall >= 120:

            score += 20

            reasons.append("Moderate rainfall")

        elif rainfall >= 60:

            score += 10

            reasons.append("Light rainfall")

        # ----------------------------------------------------
        # River Level
        # ----------------------------------------------------

        if river_level >= 95:

            score += 40

            reasons.append("River overflow")

        elif river_level >= 85:

            score += 30

            reasons.append("River near danger level")

        elif river_level >= 70:

            score += 20

            reasons.append("River level rising")

        # ----------------------------------------------------
        # Humidity
        # ----------------------------------------------------

        if humidity >= 90:

            score += 10

            reasons.append("Very high humidity")

        elif humidity >= 75:

            score += 5

            reasons.append("High humidity")

        # ----------------------------------------------------
        # Final Risk
        # ----------------------------------------------------

        if score >= 80:

            risk = "Extreme"

        elif score >= 60:

            risk = "Critical"

        elif score >= 40:

            risk = "High"

        elif score >= 20:

            risk = "Medium"

        else:

            risk = "Low"

        return RiskAssessment(

            area_id=area_id,

            area_name=area_name,

            rainfall=rainfall,

            river_level=river_level,

            humidity=humidity,

            forecast=forecast,

            risk_level=risk,

            risk_score=score,

            reason=", ".join(reasons) if reasons else "Normal weather"

        )