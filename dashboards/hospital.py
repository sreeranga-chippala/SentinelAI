"""
dashboards/hospital.py

Hospital Operations Dashboard

Visible To:
- Hospital Administrators
- Doctors
- Emergency Coordinators
"""

import pandas as pd
import streamlit as st


class HospitalDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🏥 Hospital Operations Dashboard")

        knowledge = self.world_state.get_knowledge_state()

        decision = self.world_state.get_decision_state()

        self._summary(knowledge)

        self._hospital_table(knowledge)

        self._incoming_patients(decision)

        self._assigned_missions(decision)

    # =========================================================

    def _summary(self, knowledge):

        hospitals = []

        available = 0
        occupied = 0
        icu = 0

        for area in knowledge["hospital_status"].values():

            hospitals.extend(area)

        for hospital in hospitals:

            available += hospital.available_beds

            occupied += (
                hospital.total_beds -
                hospital.available_beds
            )

            icu += hospital.icu_beds

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Hospitals",
            len(hospitals)
        )

        c2.metric(
            "Available Beds",
            available
        )

        c3.metric(
            "Occupied Beds",
            occupied
        )

        c4.metric(
            "ICU Beds",
            icu
        )

        st.divider()

    # =========================================================

    def _hospital_table(self, knowledge):

        st.subheader("Hospital Status")

        rows = []

        for hospitals in knowledge["hospital_status"].values():

            for hospital in hospitals:

                rows.append({

                    "Hospital": hospital.name,

                    "Status": hospital.status,

                    "Available Beds": hospital.available_beds,

                    "Total Beds": hospital.total_beds,

                    "ICU Beds": hospital.icu_beds,

                    "Occupancy %": hospital.occupancy_percentage

                })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No hospital information available.")

    # =========================================================

    def _incoming_patients(self, decision):

        st.subheader("Incoming Patients")

        rows = []

        allocations = decision["resource_allocations"]

        for allocation in allocations.values():

            if allocation.assigned_hospital == "None":

                continue

            rows.append({

                "Hospital": allocation.assigned_hospital,

                "Area": allocation.area_name,

                "Allocated Beds": allocation.beds_allocated

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.success("No incoming patients.")

    # =========================================================

    def _assigned_missions(self, decision):

        st.subheader("Assigned Missions")

        rows = []

        for mission in decision["missions"].values():

            rows.append({

                "Mission ID": mission.mission_id,

                "Area": mission.area_name,

                "Priority": mission.priority_level,

                "Hospital": mission.assigned_hospital,

                "Status": mission.status

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info("No missions assigned.")