import streamlit as st
import urllib.request
import base64
import cv2
import numpy as np

st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Safe Import for detection module (Member 3)
try:
    import detection
    HAS_DETECTION = True
except Exception as e:
    HAS_DETECTION = False
    DETECTION_ERROR = str(e)

# Safe Import for map module (Member 2)
try:
    import map_module
    from streamlit_folium import st_folium
    HAS_MAP = True
except Exception as e:
    HAS_MAP = False
    MAP_ERROR = str(e)

# Fetch Background Image safely as Base64 String
@st.cache_data
def get_base64_bg(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
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
            background: linear-gradient(rgba(5, 12, 22, 0.20), rgba(3, 8, 16, 0.35)), 
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

# Custom UI Styling
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    .poster-banner {
        background: rgba(10, 20, 35, 0.75);
        border: 1px solid rgba(0, 242, 254, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 18px 28px;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    div[data-testid="stVerticalBlock"] > div {
        background: rgba(8, 15, 28, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
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

# Banner Header
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

tab1, tab2 = st.tabs(["📡 Live Command Center", "🛸 3D Drone Digital Twin"])

with tab1:
    col_video, col_map = st.columns([1, 1], gap="large")
    
    # --- LEFT COLUMN: Live Webcam AI Detection Stream ---
    with col_video:
        st.subheader("🎥 Live Drone Vision Feed")
        st.caption("Thermal & Optical Survivor Detection Stream (Member 3 - detection.py)")
        
        if not HAS_DETECTION:
            st.warning(f"⚠️ Detection Module Error: {DETECTION_ERROR}")
            st.markdown("""
            <div style="height: 350px; background: rgba(3, 8, 16, 0.75); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
                [ Video Stream Container - Detection Module Missing ]
            </div>
            """, unsafe_allow_html=True)
        else:
            # Webcam Frame Capture for Streamlit Cloud
            camera_buffer = st.camera_input("Capture Live Webcam Snapshot")
            
            if 'prev_gray' not in st.session_state:
                st.session_state.prev_gray = None
            if 'alert_time' not in st.session_state:
                st.session_state.alert_time = None

            if camera_buffer is not None:
                bytes_data = camera_buffer.getvalue()
                frame = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

                # Process frame via detection.py engine
                processed_frame, st.session_state.prev_gray, st.session_state.alert_time = detection.process_frame(
                    frame, st.session_state.prev_gray, st.session_state.alert_time
                )

                st.image(processed_frame, channels="BGR", use_container_width=True)

    # --- RIGHT COLUMN: GIS Search Map ---
    with col_map:
        st.subheader("🗺️ GIS Satellite Search Grid")
        st.caption("Real-Time Drone Trajectory & Search Coverage (Member 2 - map_module.py)")
        
        if HAS_MAP and hasattr(map_module, 'get_map'):
            try:
                m = map_module.get_map()
                st_folium(m, width="100%", height=400)
            except Exception as e:
                st.error(f"Map Rendering Error: {e}")
        else:
            st.markdown("""
            <div style="height: 400px; background: rgba(3, 8, 16, 0.75); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
                [ 🛰️ Interactive Search Grid Map Loading / Module Missing ]
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 3D Digital Twin & Sensor Hardware Architecture")
    st.caption("Interactive Drone Hardware Model & Multi-Sensor Payload Array (Member 4)")
    st.components.v1.html("""
    <div style="width: 100%; height: 480px; background: rgba(3, 8, 16, 0.75); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0, 242, 254, 0.4);">
        <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
    </div>
    """, height=500)
