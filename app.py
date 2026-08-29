import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD | Tactical Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Tech Dark CSS Theme
st.markdown("""
<style>
    /* Dark Futuristic Background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1527, #050811) !important;
        color: #e2e8f0;
    }
    
    /* Title Banner Styling */
    .main-title {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    
    /* Glassmorphism Tactical Cards */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Tab Header Customization */
    button[data-baseweb="tab"] {
        font-weight: 600;
        color: #94a3b8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Header
st.markdown('<h1 class="main-title">🛸 AEROGUARD COMMAND CENTER</h1>', unsafe_allow_html=True)
st.caption("🔴 LIVE | Tactical Drone Operations & Multi-Sensor Triage Network")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📡 Live Tactical Command", 
    "⚙️ 3D Digital Twin & Sensor Array", 
    "📄 Disaster Priority Logs"
])

# TAB 1: OPERATIONAL DASHBOARD
with tab1:
    col_left, col_right = st.columns([1, 1])
    
    # Left Side: AI Thermal & Motion Detection Feed
    with col_left:
        st.subheader("🎥 Thermal & Motion Detection")
        
        # Detection Placeholder Container
        st.info("🔴 Live Stream Feed (Member 3 - detection.py)")
        
        # Audio & Detection Status Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Thermal Status", "ACTIVE", "36.8°C Target")
        m2.metric("Acoustic Sensor", "DETECTED", "+12 dB Cry")
        m3.metric("Motion Grid", "TRACKING", "Sector 4")

    # Right Side: Satellite GIS Map Grid
    with col_right:
        st.subheader("🗺️ GIS Satellite Tracking Grid")
        st.success("🛰️ Satellite Layer Active (Member 2 - map_module.py)")
        
        # Map Telemetry Details
        st.write("**Target Coordinates:** `18.5204° N, 73.8567° E`")
        st.write("**Search Grid Status:** 78% Zone Scanned")

# TAB 2: 3D DIGITAL TWIN & HARDWARE SENSORS
with tab2:
    st.subheader("🛸 Interactive 3D Drone Twin Payload")
    st.caption("Rotate, inspect, and monitor real-time drone sensor nodes (Member 4 Hardware Model)")
    
    # 3D Interactive Drone Visualization Canvas
    st.components.v1.html("""
    <div style="width: 100%; height: 380px; background: rgba(5, 8, 17, 0.8); border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #38bdf8;">
        <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
    </div>
    """, height=390)
    
    st.caption("🔗 Connected Payload Sensors: Dual Thermal FLIR | Ultrasonic Sonar | LiDAR Grid | CO2 Gas Array")

# TAB 3: DISASTER LOGS
with tab3:
    st.subheader("📊 Real-time Triage & Survivor Logs")
    st.table({
        "ID": ["#TRG-01", "#TRG-02", "#TRG-03"],
        "Priority": ["CRITICAL (Red)", "MEDIUM (Amber)", "STABLE (Green)"],
        "GPS Location": ["18.5204 N, 73.8567 E", "18.5211 N, 73.8580 E", "18.5195 N, 73.8542 E"],
        "Confidence": ["94%", "88%", "91%"]
    })
