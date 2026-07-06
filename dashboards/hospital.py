"""
dashboards/hospital.py

Hospital Operations Dashboard

Visible To:
- Hospital Administrators
- Doctors
- Emergency Coordinators
"""

import json

import streamlit as st


class HospitalDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🏥 Hospital Operations Dashboard")

        state = self.world_state.get_state()

        system = state["system"]

        self._summary(system)

        st.divider()

        self._hospital_information(state)

        st.divider()

        self._mission_plan(state)

        st.divider()

        self._public_alerts(state)

        st.divider()

        self._logs(system)

        st.divider()

        self._raw_state()

    # =========================================================

    def _summary(self, system):

        st.subheader("Hospital Operations Summary")

        statistics = system["statistics"]

        metrics = system.get("agent_metrics", {})

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Simulation Cycle",
            system["cycle"],
        )

        c2.metric(
            "Areas Processed",
            statistics["areas_processed"],
        )

        c3.metric(
            "Missions",
            statistics["missions_created"],
        )

        c4.metric(
            "Alerts",
            statistics["alerts_sent"],
        )

        if metrics:

            st.success("Hospital Agent Executed Successfully")

        else:

            st.info("Hospital Agent has not executed yet.")

    # =========================================================

    def _hospital_information(self, state):

        st.subheader("🏥 Nearby Hospitals")

        hospitals = state["input"]["hospitals"]

        if hospitals:

            st.markdown(hospitals)

        else:

            st.info("Hospital information not available.")

    # =========================================================

    def _mission_plan(self, state):

        st.subheader("🚑 Mission Planner Report")

        mission = state["decision"]["mission_plan"]

        if mission:

            st.markdown(mission)

        else:

            st.info("Mission plan not available.")

    # =========================================================

    def _public_alerts(self, state):

        st.subheader("📢 Public Alerts")

        alerts = state["decision"]["public_alerts"]

        if alerts:

            st.warning(alerts)

        else:

            st.success("No active public alerts.")

    # =========================================================

    def _logs(self, system):

        st.subheader("📜 Hospital Logs")

        logs = system["logs"]

        if not logs:

            st.info("No logs available.")

            return

        for log in reversed(logs):

            with st.expander(log["time"]):

                st.write(log["message"])

    # =========================================================

    def _raw_state(self):

        with st.expander(
            "View Raw Hospital State",
            expanded=False,
        ):

            state = self.world_state.get_state()

            st.json(

                json.loads(

                    json.dumps(
                        state,
                        default=str,
                    )

                )

            )