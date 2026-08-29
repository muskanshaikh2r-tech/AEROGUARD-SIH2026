import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time

# sounddevice audio logic
try:
    import sounddevice as sd
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False

st.set_page_config(page_title="AEROGUARD AI", layout="wide")
st.title("AEROGUARD V5 - Human + Audio + Movement")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# =========================
# AUDIO SETUP
# =========================
audio_level = 0.0

def audio_callback(indata, frames, time_info, status):
    global audio_level
    audio_level = float(np.max(np.abs(indata)))

if HAS_AUDIO:
    try:
        audio_stream = sd.InputStream(samplerate=44100, channels=1, callback=audio_callback)
        audio_stream.start()
    except Exception:
        HAS_AUDIO = False

# =========================
# LAPTOP CAMERA (0)
# =========================
camera = cv2.VideoCapture(0)

THRESHOLD = 0.15
CONFIRMATION_TIME = 0.8
alert_start_time = None
MOVEMENT_THRESHOLD = 5000
previous_gray = None

st_frame = st.empty()
run_app = st.checkbox("Start Camera", value=True)

while camera.isOpened() and run_app:
    success, frame = camera.read()
    if not success:
        st.error("Laptop Camera access nahi ho pa raha hai.")
        break

    # =========================
    # THERMAL SIMULATION
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # =========================
    # MOVEMENT DETECTION
    # =========================
    if previous_gray is None:
        previous_gray = gray.copy()
        movement_detected = False
    else:
        difference = cv2.absdiff(previous_gray, gray)
        _, movement_mask = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        movement_pixels = cv2.countNonZero(movement_mask)
        movement_detected = movement_pixels > MOVEMENT_THRESHOLD
        previous_gray = gray.copy()

    # =========================
    # HUMAN DETECTION
    # =========================
    results = model(frame, verbose=False)
    human_detected = False
    best_confidence = 0

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if class_id == 0:  # Person
                human_detected = True
                if confidence > best_confidence:
                    best_confidence = confidence

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(thermal, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(thermal, f"HUMAN {confidence * 100:.0f}%", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # =========================
    # AUDIO DETECTION
    # =========================
    audio_spike = audio_level > THRESHOLD

    # =========================
    # SURVIVOR CONDITIONS
    # =========================
    survivor_conditions = human_detected and movement_detected and audio_spike

    # =========================
    # ALERT CONFIRMATION
    # =========================
    if survivor_conditions:
        if alert_start_time is None:
            alert_start_time = time.time()
        elapsed = time.time() - alert_start_time
        confirmed_alert = elapsed >= CONFIRMATION_TIME
    else:
        alert_start_time = None
        confirmed_alert = False
        elapsed = 0

    # =========================
    # STATUS PANEL OVERLAY
    # =========================
    overlay = thermal.copy()
    cv2.rectangle(overlay, (0, 0), (440, 180), (25, 25, 25), -1)
    thermal = cv2.addWeighted(overlay, 0.85, thermal, 0.15, 0)

    cv2.putText(thermal, "AEROGUARD AI", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    human_text = f"HUMAN: DETECTED {best_confidence * 100:.0f}%" if human_detected else "HUMAN: NOT DETECTED"
    cv2.putText(thermal, human_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    movement_text = "MOVEMENT: DETECTED" if movement_detected else "MOVEMENT: NONE"
    movement_color = (0, 255, 0) if movement_detected else (255, 255, 255)
    cv2.putText(thermal, movement_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, movement_color, 2)

    audio_text = "AUDIO: SPIKE" if audio_spike else "AUDIO: NORMAL"
    audio_color = (0, 255, 255) if audio_spike else (255, 255, 255)
    cv2.putText(thermal, audio_text, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, audio_color, 2)

    cv2.putText(thermal, f"LEVEL: {audio_level:.3f}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    if survivor_conditions and not confirmed_alert:
        remaining = max(0, CONFIRMATION_TIME - elapsed)
        cv2.putText(thermal, f"VERIFYING... {remaining:.1f}s", (20, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if confirmed_alert:
        cv2.rectangle(thermal, (10, 220), (560, 285), (20, 20, 20), -1)
        cv2.rectangle(thermal, (10, 220), (560, 285), (0, 0, 255), 2)
        cv2.putText(thermal, "POSSIBLE SURVIVOR ALERT", (25, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Frame display in Streamlit
    thermal_rgb = cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)
    st_frame.image(thermal_rgb, channels="RGB", use_container_width=True)

camera.release()
if HAS_AUDIO:
    audio_stream.stop()
    audio_stream.close()
