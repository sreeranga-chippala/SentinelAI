"""
SentinelAI Coordinator

Coordinator
    ↓
Wrapper Agents
    ↓
ADK
    ↓
MCP

Production Version
"""

from __future__ import annotations

import asyncio
import time

from agents.weather_agent import WeatherAgent
from agents.traffic_agent import TrafficAgent
from agents.population_agent import PopulationAgent
from agents.hospital_agent import HospitalAgent

from agents.priority_agent import PriorityAgent
from agents.allocation_agent import AllocationAgent
from agents.decision_agent import DecisionAgent
from agents.communication_agent import CommunicationAgent


class Coordinator:

    def __init__(self, world_state):

        self.world_state = world_state

        self.weather = WeatherAgent()
        self.traffic = TrafficAgent()
        self.population = PopulationAgent()
        self.hospital = HospitalAgent()

        self.priority = PriorityAgent()
        self.allocation = AllocationAgent()
        self.decision = DecisionAgent()
        self.communication = CommunicationAgent()

    async def _run_agent(
        self,
        name: str,
        agent,
        query: str,
    ):

        start = time.perf_counter()

        try:

            result = await asyncio.to_thread(
                agent.run,
                query,
            )

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

        return result

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

        (
            weather,
            traffic,
            population,
            hospital,
        ) = await asyncio.gather(

            self._run_agent(
                "Weather",
                self.weather,
                f"""
What is the current weather in
{disaster_area}?
""",
            ),

            self._run_agent(
                "Traffic",
                self.traffic,
                f"""
Find the fastest rescue route
from Bengaluru
to {disaster_area}.
""",
            ),

            self._run_agent(
                "Population",
                self.population,
                f"""
What is the population of
{disaster_area}?
""",
            ),

            self._run_agent(
                "Hospital",
                self.hospital,
                f"""
Find nearby hospitals
in {disaster_area}.
Return only nearest hospitals.
""",
            ),

        )

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

        priority = await asyncio.to_thread(

            self.priority.run,

            f"""
Weather Information

{weather}

Traffic Information

{traffic}

Population Information

{population}

Hospital Information

{hospital}

Rank affected areas by priority.
""",
        )

        self.world_state.update_knowledge(
            "priority_scores",
            priority,
        )

        allocation = await asyncio.to_thread(

            self.allocation.run,

            f"""
Priority Report

{priority}

Allocate

- Rescue Teams
- Ambulances
- Boats
- Food
- Medical Kits
""",
        )

        self.world_state.update_decision(
            "resource_allocations",
            allocation,
        )

        decision = await asyncio.to_thread(

            self.decision.run,

            f"""
Priority

{priority}

Allocation

{allocation}

Generate disaster response mission.
""",
        )

        self.world_state.update_decision(
            "missions",
            decision,
        )

        communication = await asyncio.to_thread(

            self.communication.run,

            f"""
Mission Plan

{decision}

Generate a public emergency alert.
""",
        )

        self.world_state.update_decision(
            "public_alerts",
            communication,
        )

        self.world_state.increment_cycle()

        self.world_state.add_log(

            f"Cycle "
            f"{self.world_state.get_cycle()} "
            f"completed successfully."

        )

        self.world_state.update_system(
            "status",
            "IDLE",
        )

    def run(
        self,
        disaster_area: str,
    ):

        asyncio.run(
            self.execute_cycle(
                disaster_area,
            )
        )