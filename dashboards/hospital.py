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

        self._resource_allocations(state)

        st.divider()

        self._assigned_missions(state)

        st.divider()

        self._public_alerts(state)

        st.divider()

        self._logs(system)

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

        if not hospitals:

            st.info("Hospital information not available.")

            return

        st.markdown(hospitals)

    # =========================================================

    def _resource_allocations(self, state):

        st.subheader("🚑 Resource Allocation")

        allocation = state["decision"]["resource_allocations"]

        if not allocation:

            st.info("No resource allocations available.")

            return

        st.markdown(allocation)

    # =========================================================

    def _assigned_missions(self, state):

        st.subheader("🎯 Assigned Missions")

        missions = state["decision"]["missions"]

        if not missions:

            st.info("No missions generated.")

            return

        st.markdown(missions)

    # =========================================================

    def _public_alerts(self, state):

        st.subheader("📢 Public Alerts")

        alerts = state["decision"]["public_alerts"]

        if not alerts:

            st.success("No active public alerts.")

            return

        st.warning(alerts)

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
                        state["input"]["hospitals"],
                        default=str,
                    )
                )
            )