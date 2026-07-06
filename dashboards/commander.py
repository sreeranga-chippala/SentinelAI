"""
dashboards/commander.py

Commander Dashboard

Visible To:
- Disaster Management Authority
- Command Center
- District Collector
"""

import json

import streamlit as st


class CommanderDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("🛰️ Commander Dashboard")

        state = self.world_state.get_state()

        system = state["system"]
        statistics = system["statistics"]

        self._system_overview(system, statistics)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            self._weather(state)
            self._traffic(state)
            self._population(state)

        with col2:

            self._hospital(state)
            self._priority(state)
            self._allocation(state)

        st.divider()

        self._mission(state)

        st.divider()

        self._alerts(state)

        st.divider()

        self._logs(system)

    # =========================================================

    def _system_overview(
        self,
        system,
        statistics,
    ):

        st.subheader("System Overview")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Cycle",
            system["cycle"],
        )

        c2.metric(
            "Status",
            system["status"],
        )

        c3.metric(
            "Areas",
            statistics["areas_processed"],
        )

        c4.metric(
            "Missions",
            statistics["missions_created"],
        )

        c5.metric(
            "Alerts",
            statistics["alerts_sent"],
        )

        if system["last_updated"]:

            st.caption(
                f"Last Updated : {system['last_updated']}"
            )

    # =========================================================

    def _weather(
        self,
        state,
    ):

        st.subheader("🌦 Weather Intelligence")

        weather = state["input"]["weather"]

        if weather:

            st.markdown(weather)

        else:

            st.info("No weather information available.")

    # =========================================================

    def _traffic(
        self,
        state,
    ):

        st.subheader("🚦 Traffic Intelligence")

        roads = state["input"]["roads"]

        if roads:

            st.markdown(roads)

        else:

            st.info("No traffic information available.")

    # =========================================================

    def _population(
        self,
        state,
    ):

        st.subheader("👥 Population Intelligence")

        population = state["input"]["areas"]

        if population:

            st.markdown(population)

        else:

            st.info("No population information available.")

    # =========================================================

    def _hospital(
        self,
        state,
    ):

        st.subheader("🏥 Hospital Intelligence")

        hospitals = state["input"]["hospitals"]

        if hospitals:

            st.markdown(hospitals)

        else:

            st.info("No hospital information available.")

    # =========================================================

    def _priority(
        self,
        state,
    ):

        st.subheader("🚨 Priority Analysis")

        priority = state["knowledge"]["priority_scores"]

        if priority:

            st.markdown(priority)

        else:

            st.info("Priority analysis not available.")

    # =========================================================

    def _allocation(
        self,
        state,
    ):

        st.subheader("🚑 Resource Allocation")

        allocation = state["decision"]["resource_allocations"]

        if allocation:

            st.markdown(allocation)

        else:

            st.info("No resource allocation available.")

    # =========================================================

    def _mission(
        self,
        state,
    ):

        st.subheader("🎯 Mission Plan")

        mission = state["decision"]["missions"]

        if mission:

            st.markdown(mission)

        else:

            st.info("Mission plan not available.")

    # =========================================================

    def _alerts(
        self,
        state,
    ):

        st.subheader("📢 Public Alerts")

        alerts = state["decision"]["public_alerts"]

        if alerts:

            st.warning(alerts)

        else:

            st.success("No public alerts.")

    # =========================================================

    def _logs(
        self,
        system,
    ):

        st.subheader("📜 System Logs")

        logs = system["logs"]

        if not logs:

            st.info("No logs available.")

            return

        for log in reversed(logs):

            st.text(
                f"[{log['time']}] {log['message']}"
            )

    # =========================================================

    def _raw_state(
        self,
        state,
    ):

        with st.expander(
            "View Raw World State",
            expanded=False,
        ):

            st.json(
                json.loads(
                    json.dumps(
                        state,
                        default=str,
                    )
                )
            )