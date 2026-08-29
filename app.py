import streamlit as st

st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# High-Res Dark Cyber Drone Image via Direct Reliable Link
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(5, 12, 22, 0.82), rgba(3, 8, 16, 0.90)), 
                    url("https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=2000&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    .poster-banner {
        background: rgba(10, 20, 35, 0.75);
        border: 1px solid rgba(0, 242, 254, 0.4);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 18px 28px;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    div[data-testid="stVerticalBlock"] > div {
        background: rgba(8, 15, 28, 0.70) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }

    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        padding: 10px 24px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00f2fe !important;
        border-bottom-color: #00f2fe !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="poster-banner">
    <div>
        <span style="background: rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe; color: #00f2fe; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.75rem;">
            AI FOR SOCIAL GOOD
        </span>
        <h1 style="margin: 8px 0 0 0; color: #f8fafc; font-weight: 800; font-size: 2rem; letter-spacing: 1px;">
            🛸 AEROGUARD
        </h1>
        <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">
            Autonomous AI Drone Simulation & Disaster Rescue Command Center
        </p>
    </div>
    <div style="text-align: right;">
        <span style="background-color: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">
            🔴 LIVE RESCUE MISSION ACTIVE
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "📡 Live Command Center", 
    "🛸 3D Drone Digital Twin"
])

with tab1:
    col_video, col_map = st.columns([1, 1], gap="large")
    
    with col_video:
        st.subheader("🎥 Live Drone Vision Feed")
        st.caption("Thermal & Optical Survivor Detection Stream (Member 3 - detection.py)")
        st.markdown("""
        <div style="height: 400px; background: rgba(3, 8, 16, 0.85); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
            [ 📷 Live Video Stream Canvas Container ]
        </div>
        """, unsafe_allow_html=True)

    with col_map:
        st.subheader("🗺️ GIS Satellite Search Grid")
        st.caption("Real-Time Drone Trajectory & Search Coverage (Member 2 - map_module.py)")
        st.markdown("""
        <div style="height: 400px; background: rgba(3, 8, 16, 0.85); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
            [ 🛰️ Interactive Search Grid Map Container ]
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 3D Digital Twin & Sensor Hardware Architecture")
    st.caption("Interactive Drone Hardware Model & Multi-Sensor Payload Array (Member 4)")
    st.components.v1.html("""
    <div style="width: 100%; height: 480px; background: rgba(3, 8, 16, 0.85); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0, 242, 254, 0.4);">
        <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
    </div>
    """, height=500)
