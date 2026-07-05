"""
app.py

SentinelAI
Main Streamlit Application
"""

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from world_state import WorldState
from coordinator import Coordinator
from scheduler import Scheduler

from dashboards.commander import CommanderDashboard
from dashboards.hospital import HospitalDashboard
from dashboards.rescue import RescueDashboard
from dashboards.public import PublicDashboard


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="SentinelAI",

    page_icon="🚨",

    layout="wide",

    initial_sidebar_state="expanded"

)
st_autorefresh(
    interval=2000,
    key="sentinel_refresh"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "world_state" not in st.session_state:

    st.session_state.world_state = WorldState()

if "coordinator" not in st.session_state:

    st.session_state.coordinator = Coordinator(
        st.session_state.world_state
    )

if "scheduler" not in st.session_state:

    st.session_state.scheduler = Scheduler(
        coordinator=st.session_state.coordinator,
        interval=30
    )

world_state = st.session_state.world_state

coordinator = st.session_state.coordinator

scheduler = st.session_state.scheduler


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🚨 SentinelAI")

st.sidebar.markdown("---")

dashboard = st.sidebar.radio(

    "Dashboard",

    (

        "Commander",

        "Hospital",

        "Rescue",

        "Public"

    )

)

st.sidebar.markdown("---")

# ==========================================================
# CONTROL PANEL
# ==========================================================

st.sidebar.subheader("Simulation Controls")

if st.sidebar.button(

    "▶ Run One Cycle",

    use_container_width=True

):

    coordinator.execute_cycle()

    st.success("Simulation cycle completed.")

# ----------------------------------------------------------

if not scheduler.is_running():

    if st.sidebar.button(

        "▶ Start Auto Simulation",

        use_container_width=True

    ):

        scheduler.start()

        st.success("Scheduler Started")

else:

    if st.sidebar.button(

        "⏹ Stop Auto Simulation",

        use_container_width=True

    ):

        scheduler.stop()

        st.warning("Scheduler Stopped")

# ----------------------------------------------------------

if st.sidebar.button(

    "🔄 Reset Simulation",

    use_container_width=True

):

    scheduler.stop()

    world_state.reset()

    st.success("Simulation Reset")

st.sidebar.markdown("---")

# ==========================================================
# SYSTEM STATUS
# ==========================================================

system = world_state.get_system_state()

st.sidebar.subheader("System Status")

st.sidebar.write(

    f"**Cycle:** {system['cycle']}"

)

st.sidebar.write(

    f"**Status:** {system['status']}"

)

st.sidebar.write(

    f"**Last Updated:** {system['last_updated']}"

)

st.sidebar.markdown("---")

stats = world_state.get_statistics()

st.sidebar.subheader("Statistics")

st.sidebar.metric(

    "Areas",

    stats["areas_processed"]

)

st.sidebar.metric(

    "Missions",

    stats["missions_created"]

)

st.sidebar.metric(

    "Alerts",

    stats["alerts_sent"]

)

# ==========================================================
# ROUTING
# ==========================================================

if dashboard == "Commander":

    CommanderDashboard(

        world_state

    ).render()

elif dashboard == "Hospital":

    HospitalDashboard(

        world_state

    ).render()

elif dashboard == "Rescue":

    RescueDashboard(

        world_state

    ).render()

elif dashboard == "Public":

    PublicDashboard(

        world_state

    ).render()