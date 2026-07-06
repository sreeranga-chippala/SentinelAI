"""
SentinelAI Coordinator

Architecture

                Coordinator
                     │
        ┌────────────┼────────────┐
        │            │            │
   Weather MCP   Traffic MCP   Population MCP
        │
   Hospital MCP
        │
   (Parallel Execution)
        │
        ▼
 Mission Planner (Only Gemini Call)
        │
        ▼
     World State
"""

from __future__ import annotations

import asyncio
import time

from agents.weather_agent import WeatherAgent
from agents.traffic_agent import TrafficAgent
from agents.population_agent import PopulationAgent
from agents.hospital_agent import HospitalAgent
from agents.mission_planner_agent import MissionPlannerAgent


class Coordinator:

    def __init__(self, world_state):

        self.world_state = world_state

        self.weather = WeatherAgent()
        self.traffic = TrafficAgent()
        self.population = PopulationAgent()
        self.hospital = HospitalAgent()

        # Only reasoning LLM
        self.mission_planner = MissionPlannerAgent()

    # =====================================================
    # Execute Individual Agent
    # =====================================================

    async def _run_agent(
        self,
        name: str,
        coroutine,
    ):

        start = time.perf_counter()

        try:

            result = await coroutine

            result_text = str(result).lower()

            failure_keywords = (

                "error:",
                "unable",
                "unavailable",
                "failed",
                "failure",
                "timeout",
                "timed out",
                "cannot",
                "can't",
                "i am sorry",
                "service unavailable",
                "internal server",

            )

            success = not any(
                keyword in result_text
                for keyword in failure_keywords
            )

        except Exception as exc:

            result = f"ERROR: {exc}"

            success = False

        elapsed = round(
            time.perf_counter() - start,
            2,
        )

        self.world_state.add_log(
            f"{name} completed "
            f"(success={success}) "
            f"in {elapsed}s"
        )

        self.world_state.update_agent_metric(
            name,
            elapsed,
            success,
        )

        return result, success

    # =====================================================
    # Execute Complete Simulation
    # =====================================================

    async def execute_cycle(
        self,
        disaster_area: str,
    ):

        self.world_state.update_system(
            "status",
            "RUNNING",
        )

        self.world_state.add_log(
            f"Starting disaster cycle for {disaster_area}"
        )

        origin = "Kempegowda International Airport"

        weather_task = self._run_agent(
            "Weather",
            self.weather.run_async(
                disaster_area,
            ),
        )

        traffic_task = self._run_agent(
            "Traffic",
            self.traffic.run_async(
                origin,
                disaster_area,
            ),
        )

        population_task = self._run_agent(
            "Population",
            self.population.run_async(
                disaster_area,
            ),
        )

        hospital_task = self._run_agent(
            "Hospital",
            self.hospital.run_async(
                disaster_area,
            ),
        )

        (
            (weather, weather_ok),
            (traffic, traffic_ok),
            (population, population_ok),
            (hospital, hospital_ok),
        ) = await asyncio.gather(

            weather_task,
            traffic_task,
            population_task,
            hospital_task,

        )

        # =====================================================
        # Save MCP Outputs
        # =====================================================

        self.world_state.update_input(
            "weather",
            weather,
        )

        self.world_state.update_input(
            "roads",
            traffic,
        )

        self.world_state.update_input(
            "areas",
            population,
        )

        self.world_state.update_input(
            "hospitals",
            hospital,
        )

        # =====================================================
        # Determine if Planner can run
        # =====================================================

        mcp_failed = not all(

            (
                weather_ok,
                traffic_ok,
                population_ok,
                hospital_ok,
            )

        )

        if mcp_failed:

            mission_plan = """
# Mission Planner

Unable to generate a disaster response.

One or more MCP services failed.

Please retry the simulation.
"""

            self.world_state.update_agent_metric(

                "Mission Planner",

                0,

                False,

            )

            self.world_state.add_log(

                "Mission Planner skipped because an MCP service failed."

            )

        else:

            planner_prompt = f"""
You are SentinelAI's Mission Planner.

The following reports are trusted outputs from MCP tools.

================ WEATHER ================

{weather}

================ TRAFFIC ================

{traffic}

================ POPULATION ================

{population}

================ HOSPITAL ================

{hospital}

Using ONLY these reports generate ONE comprehensive disaster response.

Return Markdown only.

Include:

# Priority Assessment

# Resource Allocation

# Mission Plan

# Public Alert

# SMS Alert

# Radio Announcement

# TV Announcement

# Social Media Alert

Rules:

- Never invent information.
- Never modify MCP results.
- Use ONLY the supplied reports.
"""            
            mission_plan, _ = await self._run_agent(
                "Mission Planner",
                self.mission_planner.run_async(
                    planner_prompt,
                ),
            )

        # =====================================================
        # Save Planner Output
        # =====================================================

        self.world_state.update_knowledge(
            "priority_scores",
            mission_plan,
        )

        self.world_state.update_decision(
            "mission_plan",
            mission_plan,
        )

        self.world_state.update_decision(
            "public_alerts",
            mission_plan,
        )

        # =====================================================
        # Statistics
        # =====================================================

        self.world_state.increment_statistic(
            "areas_processed",
        )

        self.world_state.increment_statistic(
            "missions_created",
        )

        self.world_state.increment_statistic(
            "alerts_sent",
        )

        # =====================================================
        # Finish Cycle
        # =====================================================

        self.world_state.increment_cycle()

        self.world_state.save_cycle_snapshot()

        self.world_state.add_log(
            f"Cycle {self.world_state.get_cycle()} completed successfully."
        )

        self.world_state.update_system(
            "status",
            "IDLE",
        )

    # =====================================================
    # Public Entry Point
    # =====================================================

    def run(
        self,
        disaster_area: str,
    ):

        asyncio.run(
            self.execute_cycle(
                disaster_area,
            )
        )