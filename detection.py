import cv2
import numpy as np
from ultralytics import YOLO
import time

# PyAudio / SoundDevice Safe Import for Cloud
try:
    import sounddevice as sd
    AUDIO_SUPPORTED = True
except Exception:
    AUDIO_SUPPORTED = False

# YOLO Model Load
model = YOLO("yolov8n.pt")
THRESHOLD = 0.15
CONFIRMATION_TIME = 0.8

audio_level = 0.0
audio_stream = None

# Audio Setup with Hardware Fallback
if AUDIO_SUPPORTED:
    def audio_callback(indata, frames, time_info, status):
        global audio_level
        if not status:
            audio_level = float(np.max(np.abs(indata)))

    try:
        devices = sd.query_devices()
        input_devices = [d for d in devices if d.get('max_input_channels', 0) > 0]
        if len(input_devices) > 0:
            audio_stream = sd.InputStream(
                samplerate=44100,
                channels=1,
                callback=audio_callback
            )
            audio_stream.start()
    except Exception as e:
        print(f"Audio device not available: {e}")


def process_frame(frame, previous_gray=None, alert_start_time=None):
    global audio_level

    # 1. Thermal Simulation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # 2. Movement Detection
    movement_detected = False
    if previous_gray is not None:
        difference = cv2.absdiff(previous_gray, gray)
        _, movement_mask = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        movement_pixels = cv2.countNonZero(movement_mask)
        movement_detected = movement_pixels > 5000

    new_previous_gray = gray.copy()

    # 3. Human Detection (YOLO)
    results = model(frame, verbose=False)
    human_detected = False
    best_confidence = 0.0

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
                cv2.putText(
                    thermal,
                    f"HUMAN {confidence * 100:.0f}%",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

    # 4. Audio Spike Check
    audio_spike = audio_level > THRESHOLD if audio_stream is not None else False

    # 5. Survivor Conditions
    survivor_conditions = human_detected and movement_detected

    # 6. Alert Confirmation Logic
    confirmed_alert = False
    if survivor_conditions:
        if alert_start_time is None:
            alert_start_time = time.time()
        elapsed = time.time() - alert_start_time
        if elapsed >= CONFIRMATION_TIME:
            confirmed_alert = True
    else:
        alert_start_time = None

    # 7. Overlay UI Panel
    overlay = thermal.copy()
    cv2.rectangle(overlay, (0, 0), (440, 180), (25, 25, 25), -1)
    thermal = cv2.addWeighted(overlay, 0.85, thermal, 0.15, 0)

    cv2.putText(thermal, "AEROGUARD AI", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    human_text = f"HUMAN: DETECTED {best_confidence * 100:.0f}%" if human_detected else "HUMAN: NOT DETECTED"
    cv2.putText(thermal, human_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    movement_text = "MOVEMENT: DETECTED" if movement_detected else "MOVEMENT: NONE"
    cv2.putText(thermal, movement_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if movement_detected else (255, 255, 255), 2)

    audio_text = "AUDIO: SPIKE" if audio_spike else ("AUDIO: ACTIVE" if audio_stream else "AUDIO: N/A")
    cv2.putText(thermal, audio_text, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255) if audio_spike else (255, 255, 255), 2)

    if confirmed_alert:
        cv2.rectangle(thermal, (10, 220), (560, 285), (0, 0, 255), 2)
        cv2.putText(thermal, "POSSIBLE SURVIVOR ALERT", (25, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return thermal, new_previous_gray, alert_start_time
