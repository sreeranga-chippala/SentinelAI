"""
utils/population_analyzer.py

Analyzes population vulnerability.
"""

from models.population_assessment import PopulationAssessment


class PopulationAnalyzer:

    @staticmethod
    def analyze(area):

        score = 0

        reasons = []

        # ----------------------------------------------------
        # Children
        # ----------------------------------------------------

        if area.children >= 500:

            score += 20

            reasons.append("Large child population")

        elif area.children >= 200:

            score += 10

        # ----------------------------------------------------
        # Elderly
        # ----------------------------------------------------

        if area.elderly >= 300:

            score += 25

            reasons.append("Large elderly population")

        elif area.elderly >= 100:

            score += 15

        # ----------------------------------------------------
        # Disabled
        # ----------------------------------------------------

        if area.disabled >= 100:

            score += 20

            reasons.append("High disabled population")

        elif area.disabled >= 50:

            score += 10

        # ----------------------------------------------------
        # Rescue Requests
        # ----------------------------------------------------

        if area.rescue_requests >= 100:

            score += 30

            reasons.append("Very high rescue requests")

        elif area.rescue_requests >= 50:

            score += 20

        elif area.rescue_requests >= 20:

            score += 10

        # ----------------------------------------------------
        # Priority
        # ----------------------------------------------------

        if score >= 70:

            priority = "Extreme"

        elif score >= 50:

            priority = "High"

        elif score >= 30:

            priority = "Medium"

        else:

            priority = "Low"

        return PopulationAssessment(

            area_id=area.area_id,

            area_name=area.name,

            total_population=area.population,

            children=area.children,

            adults=area.adults,

            elderly=area.elderly,

            disabled=area.disabled,

            rescue_requests=area.rescue_requests,

            vulnerability_score=score,

            priority_level=priority,

            reason=", ".join(reasons) if reasons else "Normal population"

        )