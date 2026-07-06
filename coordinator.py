"""
SentinelAI Coordinator

Coordinator
    ↓
Wrapper Agents
    ↓
ADK
    ↓
MCP
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

        self.mission_planner = MissionPlannerAgent()

    # =========================================================

    async def _run_agent(
        self,
        name: str,
        coro,
    ):

        start = time.perf_counter()

        try:

            result = await coro

            success = True

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

        return result

    # =========================================================

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

        # =====================================================
        # Run all MCP Agents in parallel
        # =====================================================

        weather_task = self._run_agent(
            "Weather",
            self.weather.run_async(disaster_area),
        )

        traffic_task = self._run_agent(
            "Traffic",
            self.traffic.run_async(
                "Bengaluru",
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

        weather, traffic, population, hospital = await asyncio.gather(
            weather_task,
            traffic_task,
            population_task,
            hospital_task,
        )

        # =====================================================
        # Store MCP Results
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
        # Mission Planner
        # =====================================================

        mission_plan = await self._run_agent(
            "Mission Planner",
            self.mission_planner.run_async(
                f"""
Weather

{weather}

Traffic

{traffic}

Population

{population}

Hospitals

{hospital}

Generate ONE complete disaster response report.

Include:

# Priority Assessment

# Resource Allocation

# Rescue Missions

# Public Alerts

Return Markdown only.
"""
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
        # Finish
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

    # =========================================================

    def run(
        self,
        disaster_area: str,
    ):

        asyncio.run(
            self.execute_cycle(
                disaster_area,
            )
        )