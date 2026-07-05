"""
dashboards/rescue.py

Rescue Operations Dashboard

Visible To:
- NDRF
- SDRF
- Fire & Rescue
- Police
- Emergency Response Teams
"""

import pandas as pd
import streamlit as st


class RescueDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🚑 Rescue Operations Dashboard")

        knowledge = self.world_state.get_knowledge_state()

        decision = self.world_state.get_decision_state()

        self._summary(decision)

        self._mission_table(decision)

        self._resource_table(decision)

        self._route_table(knowledge)

        self._priority_table(knowledge)

    # =========================================================

    def _summary(self, decision):

        allocations = decision["resource_allocations"]

        missions = decision["missions"]

        rescue_teams = 0
        boats = 0
        ambulances = 0
        helicopters = 0

        for allocation in allocations.values():

            rescue_teams += allocation.rescue_teams
            boats += allocation.boats
            ambulances += allocation.ambulances
            helicopters += allocation.helicopters

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Active Missions",
            len(missions)
        )

        c2.metric(
            "Rescue Teams",
            rescue_teams
        )

        c3.metric(
            "Boats",
            boats
        )

        c4.metric(
            "Ambulances",
            ambulances
        )

        c5.metric(
            "Helicopters",
            helicopters
        )

        st.divider()

    # =========================================================

    def _mission_table(self, decision):

        st.subheader("Assigned Missions")

        rows = []

        for mission in decision["missions"].values():

            rows.append({

                "Mission ID": mission.mission_id,

                "Area": mission.area_name,

                "Priority": mission.priority_level,

                "Hospital": mission.assigned_hospital,

                "Teams": mission.rescue_teams,

                "Boats": mission.boats,

                "Ambulances": mission.ambulances,

                "Helicopters": mission.helicopters,

                "Status": mission.status

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No rescue missions assigned.")

    # =========================================================

    def _resource_table(self, decision):

        st.subheader("Resource Allocation")

        rows = []

        for allocation in decision["resource_allocations"].values():

            rows.append({

                "Area": allocation.area_name,

                "Hospital": allocation.assigned_hospital,

                "Beds": allocation.beds_allocated,

                "Rescue Teams": allocation.rescue_teams,

                "Boats": allocation.boats,

                "Ambulances": allocation.ambulances,

                "Helicopters": allocation.helicopters,

                "Food Packets": allocation.food_packets,

                "Medical Kits": allocation.medical_kits

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No resources allocated.")

    # =========================================================

    def _route_table(self, knowledge):

        st.subheader("Road Conditions")

        rows = []

        for routes in knowledge["route_status"].values():

            for route in routes:

                rows.append({

                    "Road": route.road_name,

                    "Status": route.route_status,

                    "Travel Time (mins)": route.travel_time

                })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No route information available.")

    # =========================================================

    def _priority_table(self, knowledge):

        st.subheader("Area Priorities")

        rows = []

        priorities = sorted(

            knowledge["priority_scores"].values(),

            key=lambda x: x.priority_score,

            reverse=True

        )

        for priority in priorities:

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