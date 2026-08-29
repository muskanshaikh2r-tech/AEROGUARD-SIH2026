import streamlit as st
import cv2
import numpy as np
import tempfile

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

# Full Screen Scaffolding & Minimal CSS
st.markdown("""
<style>
    /* Remove padding to make screen layout max-width full view */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* Dark theme containers */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(8, 15, 28, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    /* Full height video & map frames */
    .stImage > img {
        border-radius: 8px;
        width: 100% !important;
        max-height: 75vh !important;
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar Title
st.markdown("<h2 style='text-align: center; color: #00f2fe; margin-bottom: 10px;'>🛸 AEROGUARD — Live Command Center</h2>", unsafe_allow_html=True)

# Main 50-50 Split Screen Layout
col_video, col_map = st.columns([1, 1], gap="small")

# ==========================================
# LEFT HALF: Thermal Camera Detection Feed
# ==========================================
with col_video:
    st.markdown("### 🎥 Live Thermal Vision Stream")
    
    # Input Selector (Video Upload OR Webcam)
    source_type = st.radio("Select Input Source:", ["Upload Video File (MP4)", "Live Webcam Capture"], horizontal=True)

    if source_type == "Upload Video File (MP4)":
        uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov"])
        
        if uploaded_file is not None:
            # Save uploaded video to temporary file
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            cap = cv2.VideoCapture(tfile.name)
            st_frame = st.empty()
            
            run_video = st.checkbox("▶️ Play / Stream Thermal Video", value=True)
            
            prev_gray = None
            alert_time = None
            
            while run_video and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video
                    continue
                
                # Resize for performance & process
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
        # Webcam Input Mode
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

# ==========================================
# RIGHT HALF: GIS Satellite Search Grid Map
# ==========================================
with col_map:
    st.markdown("### 🗺️ GIS Search Grid & Trajectory Map")
    
    if HAS_MAP and hasattr(map_module, 'get_map'):
        try:
            m = map_module.get_map()
            st_folium(m, width="100%", height=580)
        except Exception as e:
            st.error(f"Map Rendering Error: {e}")
    else:
        st.markdown("""
        <div style="height: 580px; background: rgba(3, 8, 16, 0.85); border: 1px solid rgba(0, 242, 254, 0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #00f2fe; font-family: monospace;">
            [ 🛰️ Interactive Search Grid Map Loading ]
        </div>
        """, unsafe_allow_html=True)
