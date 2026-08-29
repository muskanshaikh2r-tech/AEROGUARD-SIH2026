import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling: Dark Glassmorphic Theme with Background Drone Watermark
st.markdown("""
<style>
    /* Full Page Background with Blurred Dark Drone Overlay */
    .stApp {
        background: linear-gradient(rgba(10, 15, 26, 0.88), rgba(5, 8, 15, 0.94)), 
                    url("https://images.unsplash.com/photo-1508614589041-895b88991e3e?q=80&w=2000&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: #e2e8f0;
    }

    /* Padding Adjustments for Clean Spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    /* Top Banner Header */
    .header-container {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 16px 24px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* High-Tech Dark Glass Cards for Main Content */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(13, 20, 36, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Tab Navigation Customization */
    button[data-baseweb="tab"] {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        padding: 10px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Header
st.markdown("""
<div class="header-container">
    <div>
        <h2 style="margin:0; color:#38bdf8; font-weight:700; font-size: 1.6rem;">🛸 AEROGUARD COMMAND CENTER</h2>
        <p style="margin:0; color:#94a3b8; font-size:0.85rem;">Autonomous Aerial Rescue & Mission Operations Dashboard</p>
    </div>
    <div style="text-align: right;">
        <span style="background-color: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;">
            🔴 LIVE MISSION ACTIVE
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Upper Navigation Bar
tab1, tab2 = st.tabs([
    "📡 Live Rescue Command", 
    "🛸 3D Drone Digital Twin"
])

# ================= TAB 1: CLEAN DASHBOARD (ONLY VIDEO & MAP) =================
with tab1:
    col_video, col_map = st.columns([1, 1], gap="large")
    
    # LEFT SIDE: DRONE CAPTURED VIDEO FEED
    with col_video:
        st.subheader("🎥 Live Drone Vision Feed")
        st.caption("Thermal & Optical Survivor Detection Stream (Member 3)")
        
        # Placeholder Space for Video Feed
        st.info("📷 Live Video Stream (`detection.py`) integrates here.")
        
        # Sample Visual Box Container
        st.markdown("""
        <div style="height: 380px; background: rgba(5, 8, 15, 0.8); border: 1px border rgba(56, 189, 248, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
            [ Live Stream Canvas Container ]
        </div>
        """, unsafe_allow_html=True)

    # RIGHT SIDE: GIS COVERED AREA MAP
    with col_map:
        st.subheader("🗺️ GIS Area Search Grid")
        st.caption("Real-Time Drone Trajectory & Search Coverage (Member 2)")
        
        # Placeholder Space for GIS Map
        st.success("🛰️ Interactive Search Grid (`map_module.py`) integrates here.")
        
        # Sample Map Canvas Container
        st.markdown("""
        <div style="height: 380px; background: rgba(5, 8, 15, 0.8); border: 1px border rgba(56, 189, 248, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8;">
            [ Interactive GIS Map Container ]
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 2: SEPARATE 3D DRONE MODEL =================
with tab2:
    st.subheader("⚙️ 3D Digital Twin & Sensor Hardware Architecture")
    st.caption("Interactive Drone Hardware Model & Payload Array (Member 4)")
    
    # Clean Full-Width 3D Model Canvas
    st.components.v1.html("""
    <div style="width: 100%; height: 480px; background: rgba(5, 8, 17, 0.85); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(56, 189, 248, 0.4);">
        <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
    </div>
    """, height=500)
