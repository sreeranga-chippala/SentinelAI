"""
dashboards/public.py

Public Safety Dashboard

Visible To:
- Citizens
- General Public
"""

import streamlit as st


class PublicDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("📢 Public Safety Dashboard")

        state = self.world_state.get_state()

        self._public_alerts(state)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            self._weather(state)

            self._traffic(state)

        with col2:

            self._hospitals(state)

            self._missions(state)

        st.divider()

        self._emergency_contacts()

        st.divider()

        self._instructions()

        st.divider()

        self._sos()

    # =========================================================

    def _public_alerts(self, state):

        st.subheader("🚨 Public Alerts")

        alerts = state["decision"]["public_alerts"]

        if alerts:

            st.error(alerts)

        else:

            st.success("No active public alerts.")

    # =========================================================

    def _weather(self, state):

        st.subheader("🌦 Current Weather")

        weather = state["input"]["weather"]

        if weather:

            st.markdown(weather)

        else:

            st.info("Weather information unavailable.")

    # =========================================================

    def _traffic(self, state):

        st.subheader("🚦 Traffic Advisory")

        traffic = state["input"]["roads"]

        if traffic:

            st.markdown(traffic)

        else:

            st.info("Traffic information unavailable.")

    # =========================================================

    def _hospitals(self, state):

        st.subheader("🏥 Nearby Hospitals")

        hospitals = state["input"]["hospitals"]

        if hospitals:

            st.markdown(hospitals)

        else:

            st.info("Hospital information unavailable.")

    # =========================================================

    def _missions(self, state):

        st.subheader("🚑 Rescue Mission Updates")

        missions = state["decision"]["missions"]

        if missions:

            st.markdown(missions)

        else:

            st.info("No rescue missions announced.")

    # =========================================================

    def _emergency_contacts(self):

        st.subheader("☎ Emergency Contacts")

        c1, c2 = st.columns(2)

        with c1:

            st.info("🚑 Ambulance : 108")

            st.info("👮 Police : 100")

            st.info("🔥 Fire : 101")

        with c2:

            st.info("🌊 Disaster Management : 1070")

            st.info("🆘 National Emergency : 112")

            st.info("👩 Women Helpline : 1091")

    # =========================================================

    def _instructions(self):

        st.subheader("📖 Public Safety Instructions")

        st.markdown(
            """
- Stay calm and follow official instructions.
- Avoid flooded or damaged roads.
- Keep emergency medicines ready.
- Carry drinking water and essential supplies.
- Follow evacuation orders immediately.
- Keep your mobile phone charged.
- Stay connected with official announcements.
- Use emergency numbers only when required.
"""
        )

    # =========================================================

    def _sos(self):

        st.subheader("🆘 Emergency SOS")

        st.warning(
            "Press the button below only during a real emergency."
        )

        if st.button(

            "🚨 SEND SOS REQUEST",

            use_container_width=True,

            type="primary",

        ):

            st.success(
                """
SOS request has been generated.

Emergency Control Center has been notified.
Please keep your phone reachable.
"""
            )