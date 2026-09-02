import os
import time
import math
import tempfile
from pathlib import Path

import streamlit as st


# Optional scientific / vision modules.
# The application keeps running even when one of these packages is unavailable.
try:
    import cv2
except Exception:
    cv2 = None

try:
    import numpy as np
except Exception:
    np = None

try:
    import folium
    from streamlit_folium import st_folium
except Exception:
    folium = None
    st_folium = None

try:
    import sounddevice as sd
except Exception:
    sd = None

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


# -------------------------------------------------------------------
# AEROGUARD — AI-POWERED EARTHQUAKE DISASTER MANAGEMENT SYSTEM
# -------------------------------------------------------------------

st.set_page_config(
    page_title="AeroGuard | Disaster Management",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
BG_IMAGE = BASE_DIR / "bg_image.png"
LOCAL_DRONE_MODEL = BASE_DIR / "drone.glb"

# You can replace this with your own hosted/local model.
# If drone.glb exists beside app.py, it is preferred.
REMOTE_DRONE_MODEL = (
    "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "HOME"

if "simulation_mode" not in st.session_state:
    st.session_state.simulation_mode = "Upload Drone Thermal MP4"

if "yolo_model" not in st.session_state:
    st.session_state.yolo_model = None


# -------------------------------------------------------------------
# GLOBAL CSS — tactical black / cyan / red / emerald interface
# -------------------------------------------------------------------

def inject_css():
    bg_uri = ""
    if BG_IMAGE.exists():
        # Streamlit's static CSS can use the local file through a data URI.
        import base64

        try:
            encoded = base64.b64encode(BG_IMAGE.read_bytes()).decode("utf-8")
            bg_uri = f"data:image/png;base64,{encoded}"
        except Exception:
            bg_uri = ""

    if bg_uri:
        background_css = f"""
        background-image:
            linear-gradient(
                rgba(2, 7, 14, 0.82),
                rgba(2, 7, 14, 0.90)
            ),
            url("{bg_uri}");
        """
    else:
        background_css = """
        background-image:
            radial-gradient(circle at 70% 25%, rgba(56,189,248,.10), transparent 28%),
            radial-gradient(circle at 25% 75%, rgba(239,68,68,.08), transparent 25%),
            linear-gradient(135deg, #02050a 0%, #07111d 50%, #02050a 100%);
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@500;600;700;800&display=swap');

        :root {{
            --cyan: #38bdf8;
            --cyan-bright: #67e8f9;
            --red: #ef4444;
            --green: #22c55e;
            --white: #eaf6ff;
            --muted: #8da3b8;
            --panel: rgba(3, 11, 20, .82);
            --border: rgba(56,189,248,.30);
        }}

        html, body, [class*="css"] {{
            font-family: 'Rajdhani', sans-serif;
        }}

        .stApp {{
            {background_css}
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            color: var(--white);
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(rgba(56,189,248,.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56,189,248,.025) 1px, transparent 1px);
            background-size: 45px 45px;
            mask-image: linear-gradient(to bottom, black, transparent 90%);
            z-index: 0;
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 1.0rem;
            padding-bottom: 2rem;
            position: relative;
            z-index: 1;
        }}

        header[data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stSidebar"] {{
            display: none;
        }}

        .topbar {{
            height: 72px;
            border-bottom: 1px solid rgba(56,189,248,.22);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 18px;
            margin-bottom: 38px;
            background: rgba(1,7,13,.52);
            backdrop-filter: blur(12px);
            clip-path: polygon(0 0, 96% 0, 100% 38%, 100% 100%, 4% 100%, 0 62%);
        }}

        .brand {{
            display: flex;
            gap: 14px;
            align-items: center;
        }}

        .brand-mark {{
            width: 46px;
            height: 46px;
            border: 1px solid var(--cyan);
            color: var(--cyan);
            display: grid;
            place-items: center;
            font-size: 25px;
            border-radius: 8px;
            box-shadow: 0 0 22px rgba(56,189,248,.20);
            background: rgba(56,189,248,.05);
        }}

        .brand-name {{
            font-family: 'Orbitron', sans-serif;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 3px;
        }}

        .brand-name span {{
            color: var(--cyan);
        }}

        .brand-sub {{
            color: #7e93a7;
            font-size: 11px;
            letter-spacing: 2.2px;
            margin-top: 2px;
        }}

        .status {{
            border: 1px solid rgba(34,197,94,.30);
            background: rgba(34,197,94,.07);
            padding: 9px 16px;
            border-radius: 7px;
            font-size: 12px;
            letter-spacing: 1.5px;
        }}

        .status-dot {{
            color: var(--green);
            text-shadow: 0 0 12px var(--green);
        }}

        .hero {{
            padding: 35px 0 20px 4%;
            min-height: 540px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .eyebrow {{
            color: var(--cyan);
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 4px;
            font-size: 17px;
            font-weight: 600;
            margin-bottom: 13px;
            text-shadow: 0 0 16px rgba(56,189,248,.35);
        }}

        .hero-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: clamp(42px, 6vw, 82px);
            line-height: .98;
            font-weight: 800;
            letter-spacing: 2px;
            margin: 0;
            color: #f5fbff;
            text-shadow: 0 4px 35px rgba(0,0,0,.75);
        }}

        .hero-title .accent {{
            color: var(--cyan);
        }}

        .hero-line {{
            width: 125px;
            height: 3px;
            margin: 26px 0 20px;
            background: linear-gradient(90deg, var(--cyan), transparent);
            box-shadow: 0 0 15px rgba(56,189,248,.6);
        }}

        .hero-copy {{
            max-width: 620px;
            color: #a9bac9;
            font-size: 18px;
            line-height: 1.45;
            letter-spacing: .35px;
        }}

        .drone-float {{
            position: absolute;
            right: 10%;
            top: 23%;
            font-size: 90px;
            opacity: .15;
            filter: drop-shadow(0 0 30px var(--cyan));
            animation: hoverDrone 4s ease-in-out infinite;
            pointer-events: none;
        }}

        @keyframes hoverDrone {{
            0%, 100% {{ transform: translateY(0) rotate(-2deg); }}
            50% {{ transform: translateY(-18px) rotate(2deg); }}
        }}

        .feature-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 24px;
        }}

        .chip {{
            border: 1px solid rgba(56,189,248,.20);
            background: rgba(3,14,25,.66);
            color: #9bb2c6;
            padding: 7px 13px;
            border-radius: 4px;
            font-size: 12px;
            letter-spacing: 1px;
        }}

        .chip b {{
            color: var(--cyan);
        }}

        .metric-panel {{
            border-top: 1px solid rgba(56,189,248,.22);
            border-bottom: 1px solid rgba(56,189,248,.16);
            background: rgba(1,7,13,.70);
            padding: 18px 25px;
            margin-top: 12px;
            backdrop-filter: blur(12px);
        }}

        .metric-label {{
            color: #6e8295;
            font-size: 11px;
            letter-spacing: 1.5px;
        }}

        .metric-value {{
            font-family: 'Orbitron', sans-serif;
            color: #e8f7ff;
            font-size: 25px;
            margin-top: 4px;
        }}

        .metric-value.green {{ color: var(--green); }}
        .metric-value.red {{ color: #ff5e5e; }}
        .metric-value.cyan {{ color: var(--cyan); }}

        .page-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 32px;
            letter-spacing: 3px;
            margin: 5px 0 6px;
        }}

        .page-subtitle {{
            color: #8fa6ba;
            margin-bottom: 22px;
        }}

        .panel {{
            border: 1px solid rgba(56,189,248,.20);
            background: rgba(2,10,18,.82);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(14px);
            box-shadow: inset 0 0 40px rgba(56,189,248,.025);
        }}

        .panel-title {{
            color: var(--cyan);
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1.5px;
            font-size: 14px;
            margin-bottom: 15px;
        }}

        .detected-card {{
            border: 1px solid rgba(239,68,68,.40);
            background: rgba(239,68,68,.07);
            border-radius: 8px;
            padding: 12px;
            margin-top: 10px;
        }}

        .live {{
            color: var(--red);
            font-weight: 700;
            letter-spacing: 1px;
        }}

        div.stButton > button {{
            width: 100%;
            min-height: 58px;
            border: 1px solid rgba(56,189,248,.42);
            background: linear-gradient(90deg, rgba(5,36,61,.95), rgba(3,16,28,.95));
            color: #e7f8ff;
            border-radius: 7px;
            font-family: 'Rajdhani', sans-serif;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1.8px;
            transition: all .2s ease;
            box-shadow: 0 0 0 rgba(56,189,248,0);
        }}

        div.stButton > button:hover {{
            border-color: var(--cyan);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 0 24px rgba(56,189,248,.18);
        }}

        .back-button div.stButton > button {{
            min-height: 44px;
            font-size: 14px;
        }}

        [data-testid="stFileUploader"] {{
            border: 1px dashed rgba(56,189,248,.28);
            border-radius: 8px;
            background: rgba(3,13,23,.60);
            padding: 8px;
        }}

        .stSelectbox label, .stRadio label, .stFileUploader label {{
            color: #9db2c5 !important;
        }}

        .map-frame {{
            border: 1px solid rgba(56,189,248,.20);
            border-radius: 8px;
            overflow: hidden;
        }}

        .model-shell {{
            border: 1px solid rgba(56,189,248,.24);
            background: rgba(0,7,14,.76);
            border-radius: 10px;
            overflow: hidden;
            min-height: 610px;
        }}

        .footer-note {{
            text-align: center;
            color: #52687b;
            font-size: 11px;
            letter-spacing: 1.2px;
            padding-top: 25px;
        }}

        .stProgress > div > div > div > div {{
            background: var(--cyan);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# -------------------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------------------

def go(page):
    st.session_state.current_page = page
    st.rerun()


def render_topbar():
    left, right = st.columns([4, 1])
    with left:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">✈</div>
                <div>
                    <div class="brand-name">AERO<span>GUARD</span></div>
                    <div class="brand-sub">AI-POWERED EARTHQUAKE DISASTER MANAGEMENT</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="status">
                SYSTEM STATUS&nbsp;&nbsp;
                <span class="status-dot">● OPERATIONAL</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_back_button():
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("←  BACK TO COMMAND CENTER", key="back_home"):
        go("HOME")
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# HOME — intentionally only TWO functional buttons
# -------------------------------------------------------------------

def render_home():
    render_topbar()

    st.markdown(
        """
        <div class="drone-float">🚁</div>

        <section class="hero">
            <div class="eyebrow">EARTHQUAKE RESPONSE • AUTONOMOUS INTELLIGENCE</div>
            <h1 class="hero-title">
                AERO<span class="accent">GUARD</span><br>
                DISASTER<br>
                COMMAND SYSTEM
            </h1>
            <div class="hero-line"></div>
            <p class="hero-copy">
                An AI-powered disaster management simulation that combines
                thermal vision, acoustic intelligence, micro-motion analysis,
                survivor detection and GIS evacuation mapping to accelerate
                earthquake rescue operations.
            </p>

            <div class="feature-strip">
                <span class="chip"><b>THERMAL</b> SURVIVOR SCAN</span>
                <span class="chip"><b>AI</b> HUMAN DETECTION</span>
                <span class="chip"><b>GIS</b> EVACUATION MAP</span>
                <span class="chip"><b>AUDIO</b> DISTRESS SIGNALS</span>
                <span class="chip"><b>MOTION</b> MICRO-MOVEMENT</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # The home page has exactly two application buttons.
    b1, b2 = st.columns(2, gap="large")

    with b1:
        if st.button("◈  VIEW 360° DRONE MODEL", key="home_3d"):
            go("3D_MODEL")

    with b2:
        if st.button("▶  START RESCUE SIMULATION", key="home_sim"):
            go("SIMULATION")

    st.markdown(
        """
        <div class="metric-panel">
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:20px;">
                <div>
                    <div class="metric-label">DRONES READY</div>
                    <div class="metric-value cyan">05 / 12</div>
                </div>
                <div>
                    <div class="metric-label">BATTERY STATUS</div>
                    <div class="metric-value green">78%</div>
                </div>
                <div>
                    <div class="metric-label">AREA COVERED</div>
                    <div class="metric-value">2.45 km²</div>
                </div>
                <div>
                    <div class="metric-label">SURVIVORS DETECTED</div>
                    <div class="metric-value red">07</div>
                </div>
                <div>
                    <div class="metric-label">EARTHQUAKE ZONE</div>
                    <div class="metric-value cyan">ACTIVE</div>
                </div>
            </div>
        </div>
        <div class="footer-note">
            AEROGUARD // TACTICAL DISASTER INTELLIGENCE PLATFORM // SIMULATION MODE
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# 3D MODEL PAGE
# -------------------------------------------------------------------

def render_3d_model():
    render_back_button()

    st.markdown(
        """
        <div class="page-title">360° DRONE MODEL</div>
        <div class="page-subtitle">
            Interactive reconnaissance drone visualization — drag to rotate,
            scroll to zoom and use the model controls.
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_src = (
        LOCAL_DRONE_MODEL.name
        if LOCAL_DRONE_MODEL.exists()
        else REMOTE_DRONE_MODEL
    )

    # model-viewer is loaded directly in the browser.
    model_html = f"""
    <script type="module"
        src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
    </script>

    <div class="model-shell">
        <model-viewer
            src="{model_src}"
            alt="AeroGuard reconnaissance drone"
            camera-controls
            auto-rotate
            auto-rotate-delay="300"
            rotation-per-second="18deg"
            shadow-intensity="1"
            exposure="0.75"
            environment-image="neutral"
            interaction-prompt="auto"
            style="width:100%;height:610px;background:
            radial-gradient(circle at 50% 42%, rgba(56,189,248,.14), transparent 34%),
            linear-gradient(180deg,#02070d,#071522);">
        </model-viewer>
    </div>
    """

    st.components.v1.html(model_html, height=625, scrolling=False)

    if not LOCAL_DRONE_MODEL.exists():
        st.info(
            "Tip: place your own `drone.glb` beside `app.py` to use a local "
            "drone model instead of the demonstration model."
        )


# -------------------------------------------------------------------
# GIS MAP
# -------------------------------------------------------------------

def create_evacuation_map():
    if folium is None:
        return None

    # Example earthquake response coordinates.
    center = [18.5204, 73.8567]

    m = folium.Map(
        location=center,
        zoom_start=14,
        tiles="CartoDB dark_matter",
        control_scale=True,
    )

    folium.Marker(
        center,
        tooltip="COMMAND CENTER",
        popup="AeroGuard Emergency Command Center",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

    survivor_points = [
        (18.5230, 73.8545, "SURVIVOR A", "High confidence"),
        (18.5182, 73.8590, "SURVIVOR B", "Thermal + motion"),
        (18.5212, 73.8620, "SURVIVOR C", "Acoustic signal"),
        (18.5165, 73.8522, "SURVIVOR D", "Thermal signature"),
    ]

    for lat, lon, name, detail in survivor_points:
        folium.Marker(
            [lat, lon],
            tooltip=name,
            popup=f"{name} — {detail}",
            icon=folium.Icon(color="red", icon="user"),
        ).add_to(m)

    # Simulated evacuation corridor.
    evacuation_route = [
        [18.5204, 73.8567],
        [18.5220, 73.8550],
        [18.5240, 73.8530],
        [18.5260, 73.8505],
    ]

    folium.PolyLine(
        evacuation_route,
        color="#38bdf8",
        weight=5,
        opacity=0.85,
        tooltip="Recommended Evacuation Corridor",
    ).add_to(m)

    # Hazard zone.
    folium.Circle(
        location=[18.5200, 73.8575],
        radius=900,
        color="#ef4444",
        fill=True,
        fill_opacity=0.10,
        tooltip="Earthquake Hazard Zone",
    ).add_to(m)

    return m


# -------------------------------------------------------------------
# AUDIO
# -------------------------------------------------------------------

def get_audio_level(duration=0.25, samplerate=16000):
    """Return RMS and peak values. Fails safely if no microphone exists."""
    if sd is None or np is None:
        return 0.0, 0.0, "sounddevice/numpy unavailable"

    try:
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        data = np.asarray(recording).flatten()

        if data.size == 0:
            return 0.0, 0.0, "no samples"

        rms = float(np.sqrt(np.mean(np.square(data))))
        peak = float(np.max(np.abs(data)))

        return rms, peak, "OK"

    except Exception as exc:
        return 0.0, 0.0, f"microphone unavailable: {exc}"


# -------------------------------------------------------------------
# YOLO
# -------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_yolo():
    if YOLO is None:
        return None, "Ultralytics is not installed."

    try:
        # YOLOv8 nano is lightweight and suitable for a prototype.
        model = YOLO("yolov8n.pt")
        return model, "YOLOv8 ready"
    except Exception as exc:
        return None, f"YOLO model unavailable: {exc}"


def process_frame(frame, model):
    """
    Thermal-style overlay + YOLO human detection.
    Returns processed frame and number of detected people.
    """
    if cv2 is None or np is None:
        return frame, 0

    display = frame.copy()
    survivor_count = 0

    # Thermal visualization.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # Blend normal image and thermal map.
    display = cv2.addWeighted(display, 0.42, thermal, 0.58, 0)

    if model is not None:
        try:
            results = model.predict(
                source=frame,
                conf=0.35,
                verbose=False,
                classes=[0],  # person
            )

            for result in results:
                if result.boxes is None:
                    continue

                for box in result.boxes:
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    conf = float(box.conf[0].cpu().numpy())

                    x1, y1, x2, y2 = xyxy.tolist()
                    survivor_count += 1

                    cv2.rectangle(
                        display,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        2,
                    )

                    label = f"SURVIVOR {conf:.0%}"
                    cv2.rectangle(
                        display,
                        (x1, max(0, y1 - 28)),
                        (x1 + 150, y1),
                        (0, 0, 255),
                        -1,
                    )
                    cv2.putText(
                        display,
                        label,
                        (x1 + 6, max(18, y1 - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

        except Exception:
            pass

    return display, survivor_count


# -------------------------------------------------------------------
# VIDEO UPLOAD MODE
# -------------------------------------------------------------------

def run_uploaded_video(uploaded_file):
    if cv2 is None or np is None:
        st.error("OpenCV and NumPy are required for video processing.")
        return

    suffix = Path(uploaded_file.name).suffix or ".mp4"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(uploaded_file.getbuffer())
        video_path = temp.name

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Could not open the uploaded video.")
        return

    video_placeholder = st.empty()
    stats_placeholder = st.empty()

    yolo_model, yolo_status = load_yolo()

    total_survivors = 0
    previous_gray = None
    frame_index = 0

    while True:
        ok, frame = cap.read()

        if not ok:
            break

        frame_index += 1

        processed, count = process_frame(frame, yolo_model)
        total_survivors = max(total_survivors, count)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        motion_score = 0.0
        if previous_gray is not None:
            diff = cv2.absdiff(previous_gray, gray)
            motion_score = float(np.mean(diff))

        previous_gray = gray

        rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        video_placeholder.image(
            rgb,
            channels="RGB",
            use_container_width=True,
        )

        stats_placeholder.markdown(
            f"""
            <div class="detected-card">
                <b class="live">● PROCESSING</b>
                &nbsp;&nbsp; Frame: {frame_index}
                &nbsp;&nbsp; | &nbsp;&nbsp; Survivors: <b>{count}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; Micro-motion: <b>{motion_score:.2f}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; {yolo_status}
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(0.015)

    cap.release()

    st.success(
        f"Video processing complete. Peak detected survivor count: {total_survivors}."
    )

    try:
        os.unlink(video_path)
    except Exception:
        pass


# -------------------------------------------------------------------
# LIVE CAMERA MODE
# -------------------------------------------------------------------

def run_live_camera():
    if cv2 is None or np is None:
        st.error("OpenCV and NumPy are required for live camera processing.")
        return

    yolo_model, yolo_status = load_yolo()

    camera_index = st.number_input(
        "Laptop camera index",
        min_value=0,
        max_value=5,
        value=0,
        step=1,
    )

    run_camera = st.checkbox(
        "ENABLE LIVE CAMERA PROCESSING",
        value=False,
    )

    video_placeholder = st.empty()
    stats_placeholder = st.empty()

    if not run_camera:
        st.info(
            "Enable the checkbox above to start the laptop camera. "
            "The browser/OS may request camera permission."
        )
        return

    cap = cv2.VideoCapture(int(camera_index))

    if not cap.isOpened():
        st.error(
            "Laptop camera could not be opened. Check camera permission, "
            "camera index, or whether another application is using it."
        )
        return

    previous_gray = None

    # Streamlit reruns the script when widgets change. This loop runs only
    # while the camera toggle remains active in the current interaction.
    for _ in range(300):
        if not st.session_state.get("current_page") == "SIMULATION":
            break

        ok, frame = cap.read()
        if not ok:
            break

        processed, survivor_count = process_frame(frame, yolo_model)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        motion_score = 0.0
        if previous_gray is not None:
            diff = cv2.absdiff(previous_gray, gray)
            motion_score = float(np.mean(diff))

        previous_gray = gray

        rms, peak, audio_status = get_audio_level()

        audio_spike = peak > 0.18 or rms > 0.08

        if audio_spike:
            audio_text = "DISTRESS AUDIO SPIKE"
        else:
            audio_text = "AUDIO NORMAL"

        rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

        video_placeholder.image(
            rgb,
            channels="RGB",
            use_container_width=True,
        )

        stats_placeholder.markdown(
            f"""
            <div class="detected-card">
                <b class="live">● LIVE</b>
                &nbsp;&nbsp; Survivors: <b>{survivor_count}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; Micro-motion: <b>{motion_score:.2f}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; RMS: <b>{rms:.3f}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; Peak: <b>{peak:.3f}</b>
                &nbsp;&nbsp; | &nbsp;&nbsp; <b>{audio_text}</b>
                <br>
                <span style="color:#7f95a9;">{audio_status} • {yolo_status}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(0.03)

    cap.release()


# -------------------------------------------------------------------
# SIMULATION PAGE
# -------------------------------------------------------------------

def render_simulation():
    render_back_button()

    st.markdown(
        """
        <div class="page-title">RESCUE SIMULATION</div>
        <div class="page-subtitle">
            Multisensor survivor detection + real-time evacuation intelligence.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown(
            '<div class="panel"><div class="panel-title">◉ SENSOR PROCESSING ENGINE</div>',
            unsafe_allow_html=True,
        )

        mode = st.radio(
            "PROCESSING MODE",
            [
                "Upload Drone Thermal MP4",
                "Live Laptop Camera + Audio",
            ],
            horizontal=True,
            key="processing_mode",
        )

        st.session_state.simulation_mode = mode

        if mode == "Upload Drone Thermal MP4":
            uploaded = st.file_uploader(
                "UPLOAD DRONE THERMAL VIDEO",
                type=["mp4", "avi", "mov", "mkv"],
                key="thermal_video",
            )

            if uploaded is not None:
                st.caption(
                    f"Loaded: {uploaded.name} • "
                    f"{uploaded.size / (1024 * 1024):.2f} MB"
                )

                if st.button(
                    "▶  PROCESS THERMAL VIDEO",
                    key="process_video",
                ):
                    run_uploaded_video(uploaded)
            else:
                st.info(
                    "Upload a drone thermal MP4 to run thermal visualization, "
                    "YOLOv8 survivor detection and frame-difference analysis."
                )

        else:
            st.markdown(
                """
                <div style="color:#8fa6ba;line-height:1.5;margin-bottom:12px;">
                    Live mode reads the laptop camera through OpenCV and
                    monitors microphone RMS/peak levels when an audio device
                    is available.
                </div>
                """,
                unsafe_allow_html=True,
            )
            run_live_camera()

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="panel"><div class="panel-title">⌖ LIVE GIS EVACUATION MAP</div>',
            unsafe_allow_html=True,
        )

        if folium is not None and st_folium is not None:
            evacuation_map = create_evacuation_map()
            st_folium(
                evacuation_map,
                width=None,
                height=585,
                returned_objects=[],
                key="aeroguard_map",
            )
        else:
            st.warning(
                "Folium map unavailable. Install `folium` and `streamlit-folium`."
            )

        st.markdown(
            """
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;">
                <span class="chip"><b>RED</b> SURVIVOR</span>
                <span class="chip"><b>CYAN</b> EVACUATION ROUTE</span>
                <span class="chip"><b>ZONE</b> EARTHQUAKE HAZARD</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# ROUTER
# -------------------------------------------------------------------

page = st.session_state.current_page

if page == "HOME":
    render_home()
elif page == "3D_MODEL":
    render_3d_model()
elif page == "SIMULATION":
    render_simulation()
else:
    st.session_state.current_page = "HOME"
    st.rerun()
