import cv2
import sounddevice as sd
import numpy as np
from ultralytics import YOLO
import time

# =========================
# AEROGUARD V4
# Alert Confirmation
# =========================

model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

audio_level = 0.0

# Minimum audio level for prototype
THRESHOLD = 0.15

# Alert must continue for this many seconds
CONFIRMATION_TIME = 0.8

alert_start_time = None


# =========================
# AUDIO CALLBACK
# =========================

def audio_callback(indata, frames, time_info, status):
    global audio_level

    if status:
        print(status)

    audio_level = float(np.max(np.abs(indata)))


# Start microphone
audio_stream = sd.InputStream(
    samplerate=44100,
    channels=1,
    callback=audio_callback
)

audio_stream.start()

print("================================")
print(" AEROGUARD V4")
print(" Alert Confirmation System")
print("================================")
print("System ready!")
print("Press Q to stop.")


# =========================
# MAIN LOOP
# =========================

while True:

    success, frame = camera.read()

    if not success:
        break

    # -------------------------
    # THERMAL SIMULATION
    # -------------------------

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thermal = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    # -------------------------
    # YOLO HUMAN DETECTION
    # -------------------------

    results = model(frame, verbose=False)

    human_detected = False
    best_confidence = 0

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # YOLO class 0 = person
            if class_id == 0:

                human_detected = True

                if confidence > best_confidence:
                    best_confidence = confidence

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # Red bounding box
                cv2.rectangle(
                    thermal,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )

                cv2.putText(
                    thermal,
                    f"HUMAN {confidence * 100:.0f}%",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

    # -------------------------
    # AUDIO DETECTION
    # -------------------------

    audio_spike = audio_level > THRESHOLD

    # -------------------------
    # ALERT CONFIRMATION
    # -------------------------

    if human_detected and audio_spike:

        # Start timer
        if alert_start_time is None:
            alert_start_time = time.time()

        elapsed = time.time() - alert_start_time

        if elapsed >= CONFIRMATION_TIME:
            confirmed_alert = True
        else:
            confirmed_alert = False

    else:

        # Conditions stopped
        alert_start_time = None
        confirmed_alert = False
        elapsed = 0

    # -------------------------
    # STATUS PANEL
    # -------------------------

    overlay = thermal.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (420, 150),
        (25, 25, 25),
        -1
    )

    thermal = cv2.addWeighted(
        overlay,
        0.85,
        thermal,
        0.15,
        0
    )

    cv2.putText(
        thermal,
        "AEROGUARD AI",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Human status
    if human_detected:

        human_text = (
            f"HUMAN: DETECTED "
            f"{best_confidence * 100:.0f}%"
        )

    else:

        human_text = "HUMAN: NOT DETECTED"

    cv2.putText(
        thermal,
        human_text,
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # Audio status
    if audio_spike:

        audio_text = "AUDIO: SPIKE"

        audio_color = (0, 255, 255)

    else:

        audio_text = "AUDIO: NORMAL"

        audio_color = (255, 255, 255)

    cv2.putText(
        thermal,
        audio_text,
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        audio_color,
        2
    )

    # Audio level
    cv2.putText(
        thermal,
        f"LEVEL: {audio_level:.3f}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    # -------------------------
    # CONFIRMATION MESSAGE
    # -------------------------

    if human_detected and audio_spike and not confirmed_alert:

        remaining = max(
            0,
            CONFIRMATION_TIME - elapsed
        )

        cv2.putText(
            thermal,
            f"VERIFYING... {remaining:.1f}s",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

    # -------------------------
    # FINAL ALERT
    # -------------------------

    if confirmed_alert:

        cv2.rectangle(
            thermal,
            (10, 190),
            (510, 250),
            (20, 20, 20),
            -1
        )

        cv2.rectangle(
            thermal,
            (10, 190),
            (510, 250),
            (0, 0, 255),
            2
        )

        cv2.putText(
            thermal,
            "POSSIBLE SURVIVOR ALERT",
            (25, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    # -------------------------
    # DISPLAY
    # -------------------------

    cv2.imshow(
        "AEROGUARD V4",
        thermal
    )

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# CLEANUP
# =========================

camera.release()

audio_stream.stop()
audio_stream.close()

cv2.destroyAllWindows()