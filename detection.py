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
CONFIRMATION_TIME = 0.5  # Quick alert confirmation for demo

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

    # 1. Thermal Simulation / Jet ColorMap Mapping
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame.copy()
        frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Enhance Contrast for FLIR Thermal detection
    enhanced_gray = cv2.equalizeHist(gray)
    thermal = cv2.applyColorMap(enhanced_gray, cv2.COLORMAP_JET)

    # 2. Movement Detection
    movement_detected = False
    if previous_gray is not None:
        difference = cv2.absdiff(previous_gray, gray)
        _, movement_mask = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)
        movement_pixels = cv2.countNonZero(movement_mask)
        movement_detected = movement_pixels > 1500  # Lower threshold for overhead drone movement

    new_previous_gray = gray.copy()

    # 3. Human Detection (YOLO with lower confidence threshold conf=0.15)
    results = model(frame, conf=0.15, verbose=False)
    human_detected = False
    best_confidence = 0.0

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Class 0 = Person (Also check for other close shapes if needed)
            if class_id == 0:
                human_detected = True
                if confidence > best_confidence:
                    best_confidence = confidence

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Draw Red Box on both Original Frame & Thermal Feed
                cv2.rectangle(thermal, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                
                label = f"SURVIVOR {confidence * 100:.0f}%"
                cv2.putText(
                    thermal,
                    label,
                    (x1, max(y1 - 8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )
                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

    # 4. Audio Spike Check
    audio_spike = audio_level > 0.15 if audio_stream is not None else False

    # 5. Survivor Conditions
    survivor_conditions = human_detected

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

    # 7. Overlay UI Panel on Thermal Video
    overlay = thermal.copy()
    cv2.rectangle(overlay, (0, 0), (420, 160), (25, 25, 25), -1)
    thermal = cv2.addWeighted(overlay, 0.85, thermal, 0.15, 0)

    cv2.putText(thermal, "AEROGUARD AI VISION", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 242, 254), 2)

    human_text = f"SURVIVORS: DETECTED ({best_confidence * 100:.0f}%)" if human_detected else "SURVIVORS: SEARCHING..."
    human_color = (0, 255, 0) if human_detected else (255, 255, 255)
    cv2.putText(thermal, human_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, human_color, 2)

    movement_text = "MOTION: DETECTED" if movement_detected else "MOTION: STABLE"
    cv2.putText(thermal, movement_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0) if movement_detected else (255, 255, 255), 2)

    audio_text = "AUDIO: SPIKE DETECTED" if audio_spike else ("AUDIO: ACTIVE" if audio_stream else "AUDIO: N/A")
    cv2.putText(thermal, audio_text, (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255) if audio_spike else (255, 255, 255), 2)

    if confirmed_alert:
        cv2.rectangle(thermal, (10, 180), (450, 230), (0, 0, 255), -1)
        cv2.putText(thermal, "🚨 SURVIVOR LOCATED!", (20, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    return thermal, new_previous_gray, alert_start_time
