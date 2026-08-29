import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time
import tempfile

st.set_page_config(page_title="AEROGUARD AI", layout="wide")
st.title("AEROGUARD V5 - Human + Audio + Movement")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# Sidebar Setup
st.sidebar.header("Input Settings")
uploaded_file = st.sidebar.file_uploader("Upload Disaster/Thermal Video", type=["mp4", "avi", "mov"])

st_frame = st.empty()

if uploaded_file is not None:
    # Uploaded file ko temp path me write karein
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    camera = cv2.VideoCapture(video_path)

    THRESHOLD = 0.15
    CONFIRMATION_TIME = 0.8
    alert_start_time = None
    MOVEMENT_THRESHOLD = 5000
    previous_gray = None

    run_app = st.sidebar.checkbox("Run Detection System", value=True)

    while camera.isOpened() and run_app:
        success, frame = camera.read()
        if not success:
            break

        # Thermal Simulation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

        # Movement Detection
        if previous_gray is None:
            previous_gray = gray.copy()
            movement_detected = False
        else:
            difference = cv2.absdiff(previous_gray, gray)
            _, movement_mask = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
            movement_pixels = cv2.countNonZero(movement_mask)
            movement_detected = movement_pixels > MOVEMENT_THRESHOLD
            previous_gray = gray.copy()

        # Human Detection
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

        # Status Panel
        overlay = thermal.copy()
        cv2.rectangle(overlay, (0, 0), (440, 150), (25, 25, 25), -1)
        thermal = cv2.addWeighted(overlay, 0.85, thermal, 0.15, 0)

        cv2.putText(thermal, "AEROGUARD AI", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        human_text = f"HUMAN: DETECTED {best_confidence * 100:.0f}%" if human_detected else "HUMAN: NOT DETECTED"
        cv2.putText(thermal, human_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        movement_text = "MOVEMENT: DETECTED" if movement_detected else "MOVEMENT: NONE"
        movement_color = (0, 255, 0) if movement_detected else (255, 255, 255)
        cv2.putText(thermal, movement_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, movement_color, 2)

        # Frame Render
        thermal_rgb = cv2.cvtColor(thermal, cv2.COLOR_BGR2RGB)
        st_frame.image(thermal_rgb, channels="RGB", use_container_width=True)

    camera.release()
else:
    st.info("Sidebar se mp4 video file upload karein detection system start karne ke liye.")
