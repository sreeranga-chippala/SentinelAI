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
    initial_sidebar_state="expanded",
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
        interval=30,
    )

world_state = st.session_state.world_state
coordinator = st.session_state.coordinator
scheduler = st.session_state.scheduler


# ==========================================================
# AUTO REFRESH
# ==========================================================

if scheduler.is_running():
    st_autorefresh(
        interval=2000,
        key="sentinel_refresh",
    )


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
        "Public",
    ),
)

st.sidebar.markdown("---")

st.sidebar.write(
    f"**Scheduler:** {'Running' if scheduler.is_running() else 'Stopped'}"
)

history = world_state.get_state()["history"]

st.sidebar.write(
    f"Snapshots: {len(history)}"
)

st.sidebar.markdown("---")


# ==========================================================
# DISASTER LOCATION
# ==========================================================

disaster_area = st.sidebar.text_input(
    "Disaster Location",
    value="Bengaluru",
)

scheduler.set_disaster_area(disaster_area)


# ==========================================================
# SIMULATION CONTROLS
# ==========================================================

st.sidebar.subheader("Simulation Controls")

if st.sidebar.button(
    "▶ Run One Cycle",
    use_container_width=True,
):
    with st.spinner("Running simulation..."):
        coordinator.run(disaster_area)

    st.success("Simulation cycle completed.")

interval = st.sidebar.slider(
    "Scheduler Interval (seconds)",
    min_value=5,
    max_value=300,
    value=scheduler.interval,
)

scheduler.set_interval(interval)

if not scheduler.is_running():

    if st.sidebar.button(
        "▶ Start Auto Simulation",
        use_container_width=True,
    ):

        scheduler.set_disaster_area(disaster_area)
        scheduler.set_interval(interval)
        scheduler.start()

        st.success("Scheduler Started")

else:

    if st.sidebar.button(
        "⏹ Stop Auto Simulation",
        use_container_width=True,
    ):

        scheduler.stop()

        st.warning("Scheduler Stopped")


if st.sidebar.button(
    "🔄 Reset Simulation",
    use_container_width=True,
):

    scheduler.stop()

    world_state.reset()

    st.session_state.world_state = world_state

    st.success("Simulation Reset")


if st.sidebar.button(
    "💾 Export World State",
    use_container_width=True,
):

    world_state.export_json()

    st.success("world_state.json exported.")

st.sidebar.markdown("---")


# ==========================================================
# SYSTEM STATUS
# ==========================================================

system = world_state.get_system_state()

st.sidebar.subheader("System Status")

st.sidebar.write(f"**Cycle:** {system['cycle']}")
st.sidebar.write(f"**Status:** {system['status']}")
st.sidebar.write(f"**Last Updated:** {system['last_updated']}")

st.sidebar.markdown("---")


# ==========================================================
# STATISTICS
# ==========================================================

stats = world_state.get_statistics()

st.sidebar.subheader("Statistics")

st.sidebar.metric(
    "Areas",
    stats["areas_processed"],
)

st.sidebar.metric(
    "Missions",
    stats["missions_created"],
)

st.sidebar.metric(
    "Alerts",
    stats["alerts_sent"],
)


# ==========================================================
# DASHBOARD ROUTING
# ==========================================================

if dashboard == "Commander":

    CommanderDashboard(world_state).render()

elif dashboard == "Hospital":

    HospitalDashboard(world_state).render()

elif dashboard == "Rescue":

    RescueDashboard(world_state).render()

elif dashboard == "Public":

    PublicDashboard(world_state).render()