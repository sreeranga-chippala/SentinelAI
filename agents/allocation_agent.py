"""
agents/allocation_agent.py

Allocation Agent

Responsibilities
----------------
1. Receive priority assessments.
2. Allocate resources for each area.
3. Prevent double allocation.
4. Return AllocationPlan objects.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent

from utils.allocation_engine import AllocationEngine


class AllocationAgent(BaseAgent):

    def __init__(
        self,
        resource_server,
        logger=None
    ):

        super().__init__(logger)

        self.resource_server = resource_server

    # ----------------------------------------------------------

    def run(
        self,
        priority_results,
        hospital_results
    ):

        self.before_run()

        resources = self.resource_server.get_resources()

        allocation_results = {}

        # ---------------------------------------------
        # Highest priority first
        # ---------------------------------------------

        ordered_priorities = sorted(

            priority_results.values(),

            key=lambda priority: priority.priority_score,

            reverse=True

        )

        # ---------------------------------------------

        for priority in ordered_priorities:

            hospitals = hospital_results.get(

                priority.area_id,

                []

            )

            plan = AllocationEngine.allocate(

                priority=priority,

                hospitals=hospitals,

                resources=resources

            )

            allocation_results[priority.area_id] = plan

            self.log(

                f"{priority.area_name} -> "

                f"{plan.message}"

            )

        self.after_run()

        return allocation_results