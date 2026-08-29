import streamlit as st
import cv2
import numpy as np
import tempfile
import urllib.request
import base64

st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Safe Import for detection module
try:
    import detection
    HAS_DETECTION = True
except Exception as e:
    HAS_DETECTION = False
    DETECTION_ERROR = str(e)

# Safe Import for map module
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

if 'is_fullscreen' not in st.session_state:
    st.session_state.is_fullscreen = False

css_padding = "0.2rem" if st.session_state.is_fullscreen else "1.5rem"
css_max_width = "100%" if st.session_state.is_fullscreen else "95%"

st.markdown(f"""
<style>
    .block-container {{
        padding-top: {css_padding} !important;
        padding-bottom: 2rem !important;
        max-width: {css_max_width} !important;
    }}

    .poster-banner {{
        background: rgba(10, 20, 35, 0.75);
        border: 1px solid rgba(0, 242, 254, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 18px 28px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    div[data-testid="stVerticalBlock"] > div {{
        background: rgba(8, 15, 28, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Header Banner
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

col_btn1, col_btn2 = st.columns([8, 2])
with col_btn2:
    if st.button("🖥️ Toggle Fullscreen View"):
        st.session_state.is_fullscreen = not st.session_state.is_fullscreen
        st.rerun()

tab1, tab2 = st.tabs(["📡 Live Command Center", "🛸 3D Drone Digital Twin"])

with tab1:
    col_video, col_map = st.columns([1, 1], gap="large")
    
    # --- LEFT COLUMN: Video Stream & YOLO Detection ---
    with col_video:
        st.subheader("🎥 Live Drone Vision Feed")
        st.caption("Thermal & Optical Survivor Detection Stream (Member 3 - detection.py)")
        
        source_type = st.radio("Input Source:", ["Upload Video File (MP4)", "Live Webcam Capture"], horizontal=True)

        if source_type == "Upload Video File (MP4)":
            uploaded_file = st.file_uploader("Upload video file...", type=["mp4", "avi", "mov"])
            
            if uploaded_file is not None:
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                
                cap = cv2.VideoCapture(tfile.name)
                st_frame = st.empty()
                run_video = st.checkbox("▶️ Start AI Detection Stream", value=True)
                
                prev_gray = None
                alert_time = None
                
                while run_video and cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Continuous Loop
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
            if HAS_DETECTION:
                camera_buffer = st.camera_input("Capture Webcam Frame")
                if camera_buffer is not None:
                    bytes_data = camera_buffer.getvalue()
                    frame = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                    
                    if 'prev_gray' not in st.session_state:
                        st.session_state.prev_gray = None
                    if 'alert_time' not in st.session_state:
                        st.session_state.alert_time = None

                    processed_frame, st.session_state.prev_gray, st.session_state.alert_time = detection.process_frame(
                        frame, st.session_state.prev_gray, st.session_state.alert_time
                    )
                    st.image(processed_frame, channels="BGR", use_container_width=True)

    # --- RIGHT COLUMN: GIS Satellite Map ---
    with col_map:
        st.subheader("🗺️ GIS Satellite Search Grid")
        st.caption("Real-Time Drone Trajectory & Search Coverage (Member 2 - map_module.py)")
        
        if HAS_MAP and hasattr(map_module, 'get_map'):
            try:
                m = map_module.get_map()
                st_folium(m, width="100%", height=520)
            except Exception as e:
                st.error(f"Map Rendering Error: {e}")
        else:
            st.markdown("""
            <div style="height: 520px; background: rgba(3, 8, 16, 0.75); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
                [ 🛰️ Interactive Search Grid Map Loading ]
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 3D Digital Twin & Sensor Hardware Architecture")
    st.components.v1.html("""
    <div style="width: 100%; height: 480px; background: rgba(3, 8, 16, 0.75); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0, 242, 254, 0.4);">
        <iframe src="https://my.spline.design/dronedemo-a3e74b3e/" frameborder="0" width="100%" height="100%"></iframe>
    </div>
    """, height=500)
