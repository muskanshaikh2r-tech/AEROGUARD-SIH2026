import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD | Disaster Command Center",
    page_icon="🛸",
    layout="wide"
)

# Main Title & Subtitle Banner
st.title("🛸 AEROGUARD: AI-Driven Disaster Rescue & Triage System")
st.caption("Autonomous Multi-Sensor Drone Simulation & Real-time GIS Mapping Dashboard")

# Top Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📡 Live Rescue Command", 
    "🧩 3D Hardware Twin & Payload", 
    "📄 Disaster Logs & Analytics"
])

# Tab 1: Main Rescue Operational View
with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("🎥 Thermal Vision & Target Detection Feed")
        st.info("AI Detection Module (Member 3 - detection.py) will render live video stream here.")
        
    with col2:
        st.subheader("🗺️ GIS Satellite Tracking & Search Grid")
        st.info("GIS Mapping Module (Member 2 - map_module.py) will render interactive map here.")

# Tab 2: Hardware Architecture & Sensor Array
with tab2:
    st.subheader("⚙️ Sensor Connectivity & 3D Drone Payload Schematic")
    st.info("Hardware Architecture (Member 4 - Tinkercad/3D CAD Payload) will be integrated here.")

# Tab 3: Data Logs & Telemetry
with tab3:
    st.subheader("📊 Survivor Priority & System Telemetry Logs")
    st.success("System Status: All Modular Services Online & Operational")
