"""
dashboards/public.py

Public Dashboard

Visible To:
- Citizens
- General Public
"""

import pandas as pd
import streamlit as st


class PublicDashboard:

    def __init__(self, world_state):

        self.world_state = world_state

    # =========================================================

    def render(self):

        st.title("📢 Public Safety Dashboard")

        knowledge = self.world_state.get_knowledge_state()

        decision = self.world_state.get_decision_state()

        self._active_alerts(decision)

        self._weather(knowledge)

        self._safe_routes(knowledge)

        self._nearest_hospitals(knowledge)

        self._emergency_contacts()

        self._instructions()

    # =========================================================

    def _active_alerts(self, decision):

        st.subheader("🚨 Active Alerts")

        alerts = decision["public_alerts"]

        if not alerts:

            st.success("✅ No active emergency alerts.")

            return

        for alert in alerts.values():

            if alert.priority_level == "Extreme":

                st.error(

                    f"""
### {alert.title}

**Area:** {alert.area_name}

{alert.message}
"""
                )

            elif alert.priority_level == "Critical":

                st.warning(

                    f"""
### {alert.title}

**Area:** {alert.area_name}

{alert.message}
"""
                )

            else:

                st.info(

                    f"""
### {alert.title}

**Area:** {alert.area_name}

{alert.message}
"""
                )

        st.divider()

    # =========================================================

    def _weather(self, knowledge):

        st.subheader("🌧 Weather Conditions")

        rows = []

        for weather in knowledge["risk_scores"].values():

            rows.append({

                "Area": weather.area_name,

                "Risk": weather.risk_level,

                "Rainfall (mm)": weather.rainfall,

                "River Level": weather.river_level,

                "Forecast": weather.forecast

            })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.info("Weather information unavailable.")

        st.divider()

    # =========================================================

    def _safe_routes(self, knowledge):

        st.subheader("🛣 Safe Routes")

        rows = []

        for routes in knowledge["route_status"].values():

            for route in routes:

                if route.route_status != "Blocked":

                    rows.append({

                        "Road": route.road_name,

                        "Status": route.route_status,

                        "Travel Time": route.travel_time

                    })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.error("No safe routes available.")

        st.divider()

    # =========================================================

    def _nearest_hospitals(self, knowledge):

        st.subheader("🏥 Nearby Hospitals")

        rows = []

        for hospitals in knowledge["hospital_status"].values():

            for hospital in hospitals:

                if hospital.available_beds > 0:

                    rows.append({

                        "Hospital": hospital.name,

                        "Available Beds": hospital.available_beds,

                        "Status": hospital.status

                    })

        if rows:

            st.dataframe(

                pd.DataFrame(rows),

                hide_index=True,

                use_container_width=True

            )

        else:

            st.warning("No hospitals currently available.")

        st.divider()

    # =========================================================

    def _emergency_contacts(self):

        st.subheader("☎ Emergency Contacts")

        col1, col2 = st.columns(2)

        with col1:

            st.info("🚑 Ambulance : 108")

            st.info("👮 Police : 100")

            st.info("🔥 Fire : 101")

        with col2:

            st.info("🌊 Disaster Management : 1070")

            st.info("👩 Women Helpline : 1091")

            st.info("🆘 National Emergency : 112")

        st.divider()

    # =========================================================

    def _instructions(self):

        st.subheader("📖 Safety Instructions")

        st.markdown("""
- Stay calm and follow official instructions.
- Move to higher ground immediately if evacuation is advised.
- Do not drive through flooded roads.
- Keep drinking water, medicines and essential documents ready.
- Switch off electricity before leaving your home.
- Use emergency numbers only for genuine emergencies.
- Follow updates from local authorities.
        """)

        st.divider()

        st.subheader("🆘 SOS")

        if st.button(
            "SEND SOS REQUEST",
            use_container_width=True
        ):

            st.success(
                "SOS request has been sent to the Emergency Control Center."
            )