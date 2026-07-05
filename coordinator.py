"""
coordinator.py

Central Orchestrator of SentinelAI

Responsibilities
----------------
1. Execute all agents in the correct order.
2. Pass outputs between agents.
3. Commit results to WorldState.
4. Increment simulation cycle.

NOTE:
Coordinator is the ONLY component allowed to modify WorldState.
"""

from agents.weather_agent import WeatherAgent
from agents.hospital_agent import HospitalAgent
from agents.traffic_agent import TrafficAgent
from agents.population_agent import PopulationAgent
from agents.priority_agent import PriorityAgent
from agents.allocation_agent import AllocationAgent
from agents.decision_agent import DecisionAgent
from agents.communication_agent import CommunicationAgent

from mcp.weather_server import WeatherServer
from mcp.hospital_server import HospitalServer
from mcp.traffic_server import TrafficServer
from mcp.population_server import PopulationServer
from mcp.resource_server import ResourceServer
from mcp.notification_server import NotificationServer


class Coordinator:

    def __init__(self, world_state):

        self.world_state = world_state

        # =====================================================
        # MCP SERVERS
        # =====================================================

        self.weather_server = WeatherServer()

        self.hospital_server = HospitalServer()

        self.traffic_server = TrafficServer()

        self.population_server = PopulationServer()

        self.resource_server = ResourceServer()

        self.notification_server = NotificationServer()

        # =====================================================
        # AGENTS
        # =====================================================

        self.weather_agent = WeatherAgent(
            weather_server=self.weather_server
        )

        self.hospital_agent = HospitalAgent(
            hospital_server=self.hospital_server
        )

        self.traffic_agent = TrafficAgent(
            traffic_server=self.traffic_server
        )

        self.population_agent = PopulationAgent(
            population_server=self.population_server
        )

        self.priority_agent = PriorityAgent()

        self.allocation_agent = AllocationAgent(
            resource_server=self.resource_server
        )

        self.decision_agent = DecisionAgent()

        self.communication_agent = CommunicationAgent(
            notification_server=self.notification_server
        )

    # =========================================================

    def execute_cycle(self):

        self.world_state.update_system(
            "status",
            "RUNNING"
        )

        # =====================================================
        # ANALYSIS LAYER
        # =====================================================

        weather_results = self.weather_agent.run()

        hospital_results = self.hospital_agent.run()

        traffic_results = self.traffic_agent.run()

        population_results = self.population_agent.run()

        # =====================================================
        # COMMIT ANALYSIS
        # =====================================================

        self.world_state.update_knowledge(
            "risk_scores",
            weather_results
        )

        self.world_state.update_knowledge(
            "hospital_status",
            hospital_results
        )

        self.world_state.update_knowledge(
            "route_status",
            traffic_results
        )

        self.world_state.update_knowledge(
            "population_status",
            population_results
        )

        # =====================================================
        # PRIORITY
        # =====================================================

        priority_results = self.priority_agent.run(

            weather_results=weather_results,

            population_results=population_results,

            hospital_results=hospital_results,

            route_results=traffic_results

        )

        self.world_state.update_knowledge(

            "priority_scores",

            priority_results

        )

        # =====================================================
        # RESOURCE ALLOCATION
        # =====================================================

        allocation_results = self.allocation_agent.run(

            priority_results=priority_results,

            hospital_results=hospital_results

        )

        # =====================================================
        # COMMIT RESOURCE ALLOCATION
        # =====================================================

        for allocation in allocation_results.values():

            if not allocation.success:
                continue

            # Reserve hospital beds

            for hospitals in self.hospital_server.get_all_hospitals().values():

                for hospital in hospitals:

                    if hospital.name == allocation.assigned_hospital:

                        self.hospital_server.reserve_beds(

                            hospital.hospital_id,

                            allocation.beds_allocated

                        )

                        break

            # Deduct resources

            self.resource_server.allocate(

                rescue_teams=allocation.rescue_teams,

                boats=allocation.boats,

                ambulances=allocation.ambulances,

                helicopters=allocation.helicopters,

                food_packets=allocation.food_packets,

                medical_kits=allocation.medical_kits

            )

            self.world_state.update_decision(

                    "resource_allocations",

                    allocation_results

                )

        # =====================================================
        # DECISION
        # =====================================================

        mission_results = self.decision_agent.run(

            priority_results=priority_results,

            allocation_results=allocation_results

        )

        self.world_state.update_decision(

            "missions",

            mission_results

        )

        # =====================================================
        # COMMUNICATION
        # =====================================================

        alert_results = self.communication_agent.run(

            mission_results=mission_results

        )

        self.world_state.update_decision(

            "public_alerts",

            alert_results

        )

        # =====================================================
        # STATISTICS
        # =====================================================

        self.world_state.update_statistics(

            "areas_processed",

            len(priority_results)

        )

        self.world_state.update_statistics(

            "missions_created",

            len(mission_results)

        )

        self.world_state.update_statistics(

            "alerts_sent",

            len(alert_results)

        )

        # =====================================================
        # LOGS
        # =====================================================

        self.world_state.add_log(

            f"Cycle {self.world_state.get_cycle() + 1} completed."

        )

        # =====================================================
        # SYSTEM
        # =====================================================

        self.world_state.increment_cycle()

        self.world_state.update_system(

            "status",

            "IDLE"

        )