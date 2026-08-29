import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Tech Sci-Fi Glassmorphism Background CSS
st.markdown("""
<style>
    /* Full Page Dark Operations Center Background */
    .stApp {
        background: linear-gradient(rgba(10, 16, 26, 0.85), rgba(5, 8, 15, 0.92)), 
                    url("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #e2e8f0;
    }
    
    /* Top Header Bar Styling */
    .top-header {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 10px;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    /* Glassmorphic Dark Floating Cards */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(13, 20, 36, 0.75) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    /* Red Emergency Indicator Badge */
    .emergency-badge {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Header
st.markdown("""
<div class="top-header">
    <span class="emergency-badge">🚨 EMERGENCY MODE ACTIVE</span>
    <h2 style="margin: 0; color: #38bdf8; font-weight: 700;">🛸 AEROGUARD COMMAND CENTER</h2>
    <span style="color: #94a3b8;">📡 Mission Time: <b>12:33 AM</b></span>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📡 Live Tactical Command", 
    "🛸 3D Hardware Twin & Payload", 
    "📄 Triage Logs & Analytics"
])

# TAB 1: LIVE TACTICAL COMMAND
with tab1:
    col_left, col_right = st.columns([1, 1])
    
    # Left Side: AI Thermal & Audio Feed
    with col_left:
        st.subheader("🎥 Thermal Vision & Target Detection Feed")
        st.info("Member 3 (detection.py) feed goes here")
        
        # Live Telemetry Sub-card
        st.subheader("📈 Telemetry Log")
        m1, m2 = st.columns(2)
        m1.metric("Detected Persons", "4", "+1")
        m2.metric("Altitude", "35m", "Stable")

    # Right Side: GIS Satellite Map Grid
    with col_right:
        st.subheader("🗺️ GIS Satellite Tracking & Search Grid")
        st.success("Member 2 (map_module.py) GIS Grid goes here")
        st.write("**Target Coordinates:** 18.52° N, 73.85° E")

# TAB 2: 3D DIGITAL TWIN
with tab2:
    st.subheader("🛸 3D Hardware Twin & Sensor Payload")
    st.caption("Interactive Drone Sensor Twin (Member 4 - Hardware Setup)")

# TAB 3: TRIAGE LOGS
with tab3:
    st.subheader("📊 Triage Log")
    st.table({
        "Label": ["RED", "AMBER", "GREEN"],
        "Timestamp": ["2026-08-29 12:43", "2026-08-29 12:33", "2026-08-29 12:31"],
        "GPS": ["18.52° N, 73.85° E", "18.52° N, 73.85° E", "18.52° N, 73.85° E"]
    })
