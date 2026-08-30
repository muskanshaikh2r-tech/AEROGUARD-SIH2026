import streamlit as st
import cv2
import numpy as np
import tempfile
import urllib.request
import base64

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Safe Imports
try:
    import detection
    HAS_DETECTION = True
except Exception as e:
    HAS_DETECTION = False
    DETECTION_ERROR = str(e)

try:
    import map_module
    from streamlit_folium import st_folium
    HAS_MAP = True
except Exception as e:
    HAS_MAP = False
    MAP_ERROR = str(e)

# Base64 Background Setup
@st.cache_data
def get_base64_bg(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return base64.b64encode(response.read()).decode()
    except Exception:
        return ""

bg_image_url = "https://i.postimg.cc/rw9dqCGj/bg-drone-png.jpg"
base64_img = get_base64_bg(bg_image_url)

if base64_img:
    bg_style = f"""
    <style>
        .stApp {{
            background: linear-gradient(rgba(3, 8, 16, 0.45), rgba(3, 8, 16, 0.65)), 
                        url("data:image/jpeg;base64,{base64_img}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            color: #e2e8f0;
        }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# CSS Customization
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 98% !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(8, 15, 28, 0.75) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #00f2fe;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Page State Setup
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# ==========================================
# PAGE 1: LANDING PAGE (ENTRY PAGE)
# ==========================================
if st.session_state.page == 'landing':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; background: rgba(5, 12, 22, 0.85); padding: 40px; border-radius: 20px; border: 2px solid #00f2fe; box-shadow: 0 0 30px rgba(0,242,254,0.3);">
            <h1 class="main-title">🛸 AEROGUARD</h1>
            <p class="sub-title">Autonomous AI Drone Simulation & Disaster Rescue Command Center</p>
            <p style="color: #cbd5e1; font-size: 0.95rem;">Real-time FLIR Thermal AI Detection • GIS Trajectory Tracking • 3D Digital Twin</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 LAUNCH COMMAND CENTER", use_container_width=True, type="primary"):
            st.session_state.page = 'dashboard'
            st.rerun()

# ==========================================
# PAGE 2: MAIN COMMAND CENTER (3 BUTTON NAVIGATION)
# ==========================================
else:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: rgba(10, 20, 35, 0.85); border-radius: 12px; border: 1px solid #00f2fe; margin-bottom: 15px;">
        <div>
            <h2 style="margin: 0; color: #00f2fe;">🛸 AEROGUARD COMMAND CENTER</h2>
        </div>
        <div>
            <span style="background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #f87171; padding: 6px 14px; border-radius: 15px; font-weight: bold; font-size: 0.8rem;">
                🔴 LIVE MISSION ACTIVE
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_tab = st.radio(
        "Navigation Menu", 
        ["ℹ️ AeroGuard Info", "🗺️ Map & Live Simulation", "⚙️ 3D Digital Twin Model"], 
        horizontal=True,
        label_visibility="collapsed"
    )

    # ----------------------------------------------------
    # TAB 1: AEROGUARD INFO
    # ----------------------------------------------------
    if nav_tab == "ℹ️ AeroGuard Info":
        st.markdown("### ℹ️ About AeroGuard Disaster Rescue System")
        
        col_info1, col_info2 = st.columns([1, 1], gap="medium")
        
        with col_info1:
            st.markdown("""
            #### 🎯 Project Overview
            **AeroGuard** is an AI-powered autonomous drone simulation framework designed for disaster response operations (Earthquakes, Floods, Collapsed Structures).
            
            * **FLIR Thermal AI Vision:** Uses YOLO computer vision models to locate trapped human survivors in zero-visibility conditions.
            * **GIS Mapping:** Real-time satellite grid positioning for rescue squad deployment.
            * **Payload Architecture:** Multi-sensor array including optical, thermal, and telemetry data.
            """)
            
        with col_info2:
            st.markdown("""
            #### 👥 Team Roles & System Architecture
            * **Member 1 (Team Leader):** Master UI Command Center, System Integration & Control Logic.
            * **Member 2 (GIS Lead):** Geolocation Satellite Search Grid & Trajectory Mapping (`map_module.py`).
            * **Member 3 (AI Lead):** Thermal Computer Vision Engine & Survivor Bounding Box (`detection.py`).
            * **Member 4 (Hardware Lead):** Interactive 3D Drone Model & Sensor Array (`Spline`).
            """)

    # ----------------------------------------------------
    # TAB 2: MAP & LIVE SIMULATION (EXACT 50-50 SPLIT VIEW)
    # ----------------------------------------------------
    elif nav_tab == "🗺️ Map & Live Simulation":
        col_video, col_map = st.columns([1, 1], gap="medium")
        
        # Left Side: FLIR Video Feed
        with col_video:
            st.markdown("#### 🎥 FLIR Thermal Vision Stream")
            uploaded_file = st.file_uploader("Upload Drone Thermal Video (.mp4)", type=["mp4", "avi", "mov"])
            
            if uploaded_file is not None:
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                
                cap = cv2.VideoCapture(tfile.name)
                st_frame = st.empty()
                run_video = st.checkbox("▶️ Run AI Survivor Detection", value=True)
                
                prev_gray = None
                alert_time = None
                
                while run_video and cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    
                    frame = cv2.resize(frame, (640, 480))
                    
                    if HAS_DETECTION:
                        processed_frame, prev_gray, alert_time = detection.process_frame(
                            frame, prev_gray, alert_time
                        )
                        st_frame.image(processed_frame, channels="BGR", use_container_width=True)
                    else:
                        st_frame.image(frame, channels="BGR", use_container_width=True)
                cap.release()
            else:
                st.info("👆 Please upload the Thermal MP4 Video file to start live AI detection stream.")

        # Right Side: Satellite Map View
        with col_map:
            st.markdown("#### 🗺️ GPS Topographical Satellite Map")
            if HAS_MAP and hasattr(map_module, 'get_map'):
                try:
                    m = map_module.get_map()
                    st_folium(m, width="100%", height=500)
                except Exception as e:
                    st.error(f"Map Rendering Note: {e}")
            else:
                st.markdown("""
                <div style="height: 500px; background: rgba(3, 8, 16, 0.85); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
                    [ 🛰️ Interactive GPS Search Grid Container Loading ]
                </div>
                """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 3: 3D DIGITAL TWIN
    # ----------------------------------------------------
    elif nav_tab == "⚙️ 3D Digital Twin Model":
        st.markdown("#### ⚙️ 3D Drone Hardware Model & Sensor Payload")
        st.caption("Interactive hardware visualization and multi-sensor connectivity dashboard.")
        
        st.components.v1.html("""
        <div style="width: 100%; height: 500px; background: rgba(3, 8, 16, 0.75); border-radius: 12px; border: 1px solid rgba(0, 242, 254, 0.4);">
            <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
        </div>
        """, height=520)
