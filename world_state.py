"""
world_state.py

Central shared state for SentinelAI.

Architecture Rules
------------------
1. Only Coordinator modifies WorldState.
2. Agents NEVER modify WorldState.
3. Agents only return results.
4. Dashboard is read-only.
"""

from copy import deepcopy
from datetime import datetime


class WorldState:

    def __init__(self):
        self.reset()

    # ==========================================================
    # INITIALIZE
    # ==========================================================

    def reset(self):

        self.state = {

            # --------------------------------------------------
            # INPUT LAYER
            # --------------------------------------------------

            "input": {

                "areas": {},

                "weather": {},

                "roads": {},

                "hospitals": {},

                "resources": {}

            },

            # --------------------------------------------------
            # KNOWLEDGE LAYER
            # --------------------------------------------------

            "knowledge": {

                "risk_scores": {},

                "population_status": {},

                "route_status": {},

                "hospital_status": {},

                "priority_scores": {}

            },

            # --------------------------------------------------
            # DECISION LAYER
            # --------------------------------------------------

            "decision": {

                "resource_allocations": {},

                "missions": {},

                "public_alerts": {}

            },

            # --------------------------------------------------
            # SYSTEM
            # --------------------------------------------------

            "system": {

                "cycle": 0,

                "status": "IDLE",

                "last_updated": None,

                "logs": [],

                "statistics": {

                    "areas_processed": 0,

                    "missions_created": 0,

                    "alerts_sent": 0

                }

            }

        }

    # ==========================================================
    # INPUT
    # ==========================================================

    def update_input(self, key, value):

        if key not in self.state["input"]:
            raise KeyError(f"Invalid input key: {key}")

        self.state["input"][key] = value

        self._touch()

    def get_input_state(self):

        return deepcopy(self.state["input"])

    # ==========================================================
    # KNOWLEDGE
    # ==========================================================

    def update_knowledge(self, key, value):

        if key not in self.state["knowledge"]:
            raise KeyError(f"Invalid knowledge key: {key}")

        self.state["knowledge"][key] = value

        self._touch()

    def get_knowledge_state(self):

        return deepcopy(self.state["knowledge"])

    def clear_knowledge(self):

        for key in self.state["knowledge"]:
            self.state["knowledge"][key] = {}

        self._touch()

    # ==========================================================
    # DECISION
    # ==========================================================

    def update_decision(self, key, value):

        if key not in self.state["decision"]:
            raise KeyError(f"Invalid decision key: {key}")

        self.state["decision"][key] = value

        self._touch()

    def get_decision_state(self):

        return deepcopy(self.state["decision"])

    def clear_decision(self):

        for key in self.state["decision"]:
            self.state["decision"][key] = {}

        self._touch()

    # ==========================================================
    # SYSTEM
    # ==========================================================

    def increment_cycle(self):

        self.state["system"]["cycle"] += 1

        self._touch()

    def get_cycle(self):

        return self.state["system"]["cycle"]

    def get_last_updated(self):

        return self.state["system"]["last_updated"]

    def get_system_state(self):

        return deepcopy(self.state["system"])

    def update_system(self, key, value):

        if key not in self.state["system"]:
            raise KeyError(f"Invalid system key: {key}")

        self.state["system"][key] = value

        self._touch()

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def update_statistics(self, key, value):

        if key not in self.state["system"]["statistics"]:
            raise KeyError(f"Invalid statistics key: {key}")

        self.state["system"]["statistics"][key] = value

        self._touch()

    def increment_statistic(self, key, amount=1):

        if key not in self.state["system"]["statistics"]:
            raise KeyError(f"Invalid statistics key: {key}")

        self.state["system"]["statistics"][key] += amount

        self._touch()

    def get_statistics(self):

        return deepcopy(self.state["system"]["statistics"])

    # ==========================================================
    # LOGGING
    # ==========================================================

    def add_log(self, message):

        self.state["system"]["logs"].append({

            "time": datetime.now(),

            "message": message

        })

    def get_logs(self):

        return deepcopy(self.state["system"]["logs"])

    def clear_logs(self):

        self.state["system"]["logs"].clear()

    # ==========================================================
    # COMPLETE STATE
    # ==========================================================

    def get_state(self):

        return deepcopy(self.state)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _touch(self):

        self.state["system"]["last_updated"] = datetime.now()