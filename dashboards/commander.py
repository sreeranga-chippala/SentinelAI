"""
dashboards/commander.py

Commander Dashboard

Visible To:
- Disaster Management Authority
- Command Center
- District Collector
"""

import pandas as pd
import streamlit as st


class CommanderDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🛰️ Commander Dashboard")

        knowledge = self.world_state.get_knowledge_state()

        decision = self.world_state.get_decision_state()

        system = self.world_state.get_system_state()

        statistics = self.world_state.get_statistics()

        self._system_overview(system, statistics)

        self._priority_table(knowledge)

        self._weather_table(knowledge)

        self._hospital_table(knowledge)

        self._route_table(knowledge)

        self._resource_table(decision)

        self._mission_table(decision)

        self._alert_table(decision)

        self._logs()

    # =========================================================

    def _system_overview(self, system, statistics):

        st.subheader("System Overview")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Cycle",
            system["cycle"]
        )

        c2.metric(
            "Status",
            system["status"]
        )

        c3.metric(
            "Areas",
            statistics["areas_processed"]
        )

        c4.metric(
            "Missions",
            statistics["missions_created"]
        )

        c5.metric(
            "Alerts",
            statistics["alerts_sent"]
        )

        st.divider()

    # =========================================================

    def _priority_table(self, knowledge):

        st.subheader("Priority Assessment")

        rows = []

        for priority in knowledge["priority_scores"].values():

            rows.append({

                "Area": priority.area_name,

                "Priority": priority.priority_level,

                "Score": priority.priority_score,

                "Recommended Action": priority.recommended_action

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No priority assessments available.")

    # =========================================================

    def _weather_table(self, knowledge):

        st.subheader("Weather Analysis")

        rows = []

        for weather in knowledge["risk_scores"].values():

            rows.append({

                "Area": weather.area_name,

                "Risk Level": weather.risk_level,

                "Risk Score": weather.risk_score,

                "Rainfall": weather.rainfall,

                "River Level": weather.river_level

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No weather information.")

    # =========================================================

    def _hospital_table(self, knowledge):

        st.subheader("Hospital Status")

        rows = []

        for hospitals in knowledge["hospital_status"].values():

            for hospital in hospitals:

                rows.append({

                    "Hospital": hospital.name,

                    "Status": hospital.status,

                    "Beds Available": hospital.available_beds,

                    "Occupancy %": hospital.occupancy_percentage

                })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No hospital information.")

    # =========================================================

    def _route_table(self, knowledge):

        st.subheader("Road Status")

        rows = []

        for routes in knowledge["route_status"].values():

            for route in routes:

                rows.append({

                    "Road": route.road_name,

                    "Status": route.route_status,

                    "Travel Time": route.travel_time

                })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No traffic information.")

    # =========================================================

    def _resource_table(self, decision):

        st.subheader("Resource Allocation")

        rows = []

        for allocation in decision["resource_allocations"].values():

            rows.append({

                "Area": allocation.area_name,

                "Hospital": allocation.assigned_hospital,

                "Beds": allocation.beds_allocated,

                "Teams": allocation.rescue_teams,

                "Boats": allocation.boats,

                "Ambulances": allocation.ambulances,

                "Helicopters": allocation.helicopters

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No allocations available.")

    # =========================================================

    def _mission_table(self, decision):

        st.subheader("Mission Control")

        rows = []

        for mission in decision["missions"].values():

            rows.append({

                "Mission ID": mission.mission_id,

                "Area": mission.area_name,

                "Priority": mission.priority_level,

                "Status": mission.status,

                "Hospital": mission.assigned_hospital

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No missions available.")

    # =========================================================

    def _alert_table(self, decision):

        st.subheader("Public Alerts")

        alerts = decision["public_alerts"]

        if not alerts:

            st.success("No active alerts.")

            return

        for alert in alerts.values():

            st.warning(

                f"""
### {alert.title}

**Area:** {alert.area_name}

**Priority:** {alert.priority_level}

**Message:** {alert.message}

**Status:** {alert.status}
"""
            )

    # =========================================================

    def _logs(self):

        st.subheader("System Logs")

        logs = self.world_state.get_logs()

        if not logs:

            st.info("No logs available.")

            return

        for log in reversed(logs):

            st.text(

                f"[{log['time']}] {log['message']}"

            )