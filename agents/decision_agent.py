"""
agents/decision_agent.py

Decision Agent

Responsibilities
----------------
1. Receive PriorityAssessment and AllocationPlan.
2. Generate executable Mission objects.
3. Return Mission objects.

NOTE:
This agent NEVER modifies WorldState.
Coordinator commits the returned results.
"""

from agents.base_agent import BaseAgent

from utils.decision_engine import DecisionEngine


class DecisionAgent(BaseAgent):

    def __init__(
        self,
        logger=None
    ):

        super().__init__(logger)

    # ----------------------------------------------------------

    def run(
        self,
        priority_results,
        allocation_results
    ):

        self.before_run()

        mission_results = {}

        for area_id, allocation in allocation_results.items():

            priority = priority_results.get(area_id)

            if priority is None:

                self.log(
                    f"Skipping {area_id}: PriorityAssessment not found."
                )

                continue

            if not allocation.success:

                self.log(
                    f"{priority.area_name} -> Allocation failed."
                )

                continue

            mission = DecisionEngine.create_mission(

                priority=priority,

                allocation=allocation

            )

            mission_results[area_id] = mission

            self.log(

                f"Mission created -> "

                f"{mission.area_name}"

            )

        self.after_run()

        return mission_results