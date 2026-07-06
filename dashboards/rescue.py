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

import streamlit as st


class RescueDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🚑 Rescue Operations Dashboard")

        state = self.world_state.get_state()

        system = state["system"]

        self._summary(system)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            self._priority(state)

            self._traffic(state)

        with col2:

            self._weather(state)

            self._hospitals(state)

        st.divider()

        self._resource_allocations(state)

        st.divider()

        self._missions(state)

        st.divider()

        self._logs(system)

    # =========================================================

    def _summary(self, system):

        st.subheader("Rescue Operations Summary")

        statistics = system["statistics"]

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

        st.caption(
            f"System Status : {system['status']}"
        )

    # =========================================================

    def _priority(self, state):

        st.subheader("🚨 Priority Analysis")

        priority = state["knowledge"]["priority_scores"]

        if priority:

            st.markdown(priority)

        else:

            st.info("Priority analysis unavailable.")

    # =========================================================

    def _traffic(self, state):

        st.subheader("🚦 Traffic Conditions")

        traffic = state["input"]["roads"]

        if traffic:

            st.markdown(traffic)

        else:

            st.info("Traffic information unavailable.")

    # =========================================================

    def _weather(self, state):

        st.subheader("🌧 Weather Conditions")

        weather = state["input"]["weather"]

        if weather:

            st.markdown(weather)

        else:

            st.info("Weather information unavailable.")

    # =========================================================

    def _hospitals(self, state):

        st.subheader("🏥 Nearby Hospitals")

        hospitals = state["input"]["hospitals"]

        if hospitals:

            st.markdown(hospitals)

        else:

            st.info("Hospital information unavailable.")

    # =========================================================

    def _resource_allocations(self, state):

        st.subheader("🚒 Resource Allocation")

        allocation = state["decision"]["resource_allocations"]

        if allocation:

            st.markdown(allocation)

        else:

            st.info("No resource allocation available.")

    # =========================================================

    def _missions(self, state):

        st.subheader("🎯 Rescue Missions")

        missions = state["decision"]["missions"]

        if missions:

            st.markdown(missions)

        else:

            st.info("No rescue missions available.")

    # =========================================================

    def _logs(self, system):

        st.subheader("📜 Rescue Logs")

        logs = system["logs"]

        if not logs:

            st.info("No logs available.")

            return

        for log in reversed(logs):

            with st.expander(log["time"]):

                st.write(log["message"])