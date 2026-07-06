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
from threading import Lock
import json


class WorldState:

    def __init__(self):

        self._lock = Lock()

        self.reset()

    # ==========================================================
    # INITIALIZE
    # ==========================================================

    def reset(self):

        self.state = {

            # --------------------------------------------------
            # INPUT
            # --------------------------------------------------

            "input": {

                "areas": "",

                "weather": "",

                "roads": "",

                "hospitals": "",

                "resources": ""

            },

            # --------------------------------------------------
            # KNOWLEDGE
            # --------------------------------------------------

           "knowledge": {

                "risk_scores": "",

                "population_status": "",

                "route_status": "",

                "hospital_status": "",

                "priority_scores": ""

            },

            # --------------------------------------------------
            # DECISION
            # --------------------------------------------------

            "decision": {

                "mission_plan": "",

                "public_alerts": ""

            },

            # --------------------------------------------------
            # HISTORY
            # --------------------------------------------------

            "history": [],

            # --------------------------------------------------
            # SYSTEM
            # --------------------------------------------------

            "system": {

                "cycle": 0,

                "status": "IDLE",

                "last_updated": None,

                "logs": [],

                "agent_metrics": {},

                "statistics": {

                    "areas_processed": 0,

                    "missions_created": 0,

                    "alerts_sent": 0,

                }

            }

        }

    # ==========================================================
    # INPUT
    # ==========================================================

    def update_input(self, key, value):

        if key not in self.state["input"]:

            raise KeyError(f"Invalid input key: {key}")

        with self._lock:

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

        with self._lock:

            self.state["knowledge"][key] = value

            self._touch()

    def get_knowledge_state(self):

        return deepcopy(self.state["knowledge"])

    def clear_knowledge(self):

        with self._lock:

            for key in self.state["knowledge"]:

                self.state["knowledge"][key] = ""

            self._touch()

    # ==========================================================
    # DECISION
    # ==========================================================

    def update_decision(self, key, value):

        if key not in self.state["decision"]:

            raise KeyError(f"Invalid decision key: {key}")

        with self._lock:

            self.state["decision"][key] = value

            self._touch()

    def get_decision_state(self):

        return deepcopy(self.state["decision"])

    def clear_decision(self):

        with self._lock:

            for key in self.state["decision"]:

                self.state["decision"][key] = ""

            self._touch()

    # ==========================================================
    # SYSTEM
    # ==========================================================

    def increment_cycle(self):

        with self._lock:

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

        with self._lock:

            self.state["system"][key] = value

            self._touch()

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def update_statistics(self, key, value):

        if key not in self.state["system"]["statistics"]:

            raise KeyError(f"Invalid statistics key: {key}")

        with self._lock:

            self.state["system"]["statistics"][key] = value

            self._touch()

    def increment_statistic(self, key, amount=1):

        if key not in self.state["system"]["statistics"]:

            raise KeyError(f"Invalid statistics key: {key}")

        with self._lock:

            self.state["system"]["statistics"][key] += amount

            self._touch()

    def get_statistics(self):

        return deepcopy(self.state["system"]["statistics"])

    # ==========================================================
    # LOGGING
    # ==========================================================

    def add_log(self, message):

        with self._lock:

            self.state["system"]["logs"].append(

                {

                    "time": datetime.now().isoformat(),

                    "message": message,

                }

            )

            self._touch()

    def get_logs(self):

        return deepcopy(self.state["system"]["logs"])

    def clear_logs(self):

        with self._lock:

            self.state["system"]["logs"].clear()

            self._touch()

    # ==========================================================
    # AGENT METRICS
    # ==========================================================

    def update_agent_metric(

        self,

        agent,

        execution_time,

        success,

    ):

        with self._lock:

            self.state["system"]["agent_metrics"][agent] = {

                "execution_time": execution_time,

                "success": success,

                "updated": datetime.now().isoformat(),

            }

            self._touch()

    def get_agent_metrics(self):

        return deepcopy(
            self.state["system"]["agent_metrics"]
        )

    # ==========================================================
    # SNAPSHOTS
    # ==========================================================

    def save_cycle_snapshot(self):

        with self._lock:

            self.state["history"].append(

                {

                    "cycle": self.get_cycle(),

                    "timestamp": datetime.now().isoformat(),

                    "input": deepcopy(self.state["input"]),

                    "knowledge": deepcopy(self.state["knowledge"]),

                    "decision": deepcopy(self.state["decision"]),

                    "system": deepcopy(self.state["system"]),

                }

            )

            self._touch()

    # ==========================================================
    # EXPORT / IMPORT
    # ==========================================================

    def export_json(

        self,

        filename="world_state.json",

    ):

        with self._lock:

            with open(

                filename,

                "w",

                encoding="utf-8",

            ) as f:

                json.dump(
                    self.state,
                    f,
                    indent=4,
                    default=str,
                )

    def load_json(

        self,

        filename,

    ):

        with self._lock:

            with open(

                filename,

                "r",

                encoding="utf-8",

            ) as f:

                self.state = json.load(f)

    # ==========================================================
    # COMPLETE STATE
    # ==========================================================

    def get_state(self):

        return deepcopy(self.state)

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _touch(self):

        self.state["system"]["last_updated"] = datetime.now().isoformat()