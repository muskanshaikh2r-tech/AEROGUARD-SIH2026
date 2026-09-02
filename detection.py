import cv2
import numpy as np
from ultralytics import YOLO
import time
import sounddevice as sd
import threading


# ============================================================
#                  AEROGUARD AI SYSTEM
# ============================================================

print("==========================================")
print("          AEROGUARD AI SYSTEM")
print("==========================================")
print("Starting system...")


# ============================================================
# 1. LOAD YOLO MODEL
# ============================================================

print("Loading YOLO model...")

model = YOLO("yolov8n.pt")

print("YOLO model loaded successfully.")


# ============================================================
# 2. AUDIO SYSTEM
# ============================================================

audio_level = 0.0
audio_peak = 0.0
audio_supported = False
audio_stream = None


def audio_callback(indata, frames, time_info, status):
    global audio_level
    global audio_peak

    if status:
        print("Audio status:", status)

    if len(indata) > 0:
        # RMS gives a stable measurement of sound level
        rms = float(np.sqrt(np.mean(indata ** 2)))

        # Peak detects sudden loud sounds
        peak = float(np.max(np.abs(indata)))

        audio_level = rms
        audio_peak = peak


print("Checking microphone...")

try:

    devices = sd.query_devices()

    input_devices = []

    for i, device in enumerate(devices):

        if device["max_input_channels"] > 0:

            input_devices.append(i)

            print(
                f"Microphone {i}: "
                f"{device['name']}"
            )

    if len(input_devices) > 0:

        # Use the default microphone
        audio_stream = sd.InputStream(
            samplerate=44100,
            channels=1,
            dtype="float32",
            callback=audio_callback,
            blocksize=1024
        )

        audio_stream.start()

        audio_supported = True

        print("Microphone started successfully.")

    else:

        print("WARNING: No microphone found.")

except Exception as e:

    print("WARNING: Microphone could not be started.")
    print("Audio error:", e)


# ============================================================
# 3. CAMERA SETUP
# ============================================================

print("Opening laptop camera...")

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Camera could not be opened.")

    if audio_stream is not None:
        audio_stream.stop()
        audio_stream.close()

    exit()


# Camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

print("Camera started successfully.")
print()
print("==========================================")
print("AEROGUARD IS READY")
print("Move in front of the camera.")
print("Make a loud sound to test audio.")
print("Press Q to quit.")
print("==========================================")


# ============================================================
# 4. MOVEMENT VARIABLES
# ============================================================

previous_gray = None

# Number of pixels that must change
MOVEMENT_THRESHOLD = 500


# ============================================================
# 5. AUDIO THRESHOLDS
# ============================================================

# These are intentionally lower for demonstration.
AUDIO_RMS_THRESHOLD = 0.05
AUDIO_PEAK_THRESHOLD = 0.15


# ============================================================
# 6. ALERT SETTINGS
# ============================================================

alert_start_time = None

CONFIRMATION_TIME = 0.5


# ============================================================
# 7. MAIN CAMERA LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # Read camera frame
    # --------------------------------------------------------

    ret, frame = cap.read()

    if not ret:

        print("ERROR: Could not read camera frame.")

        break


    # Resize
    frame = cv2.resize(
        frame,
        (960, 540)
    )


    # --------------------------------------------------------
    # MIRROR CAMERA
    # --------------------------------------------------------

    frame = cv2.flip(
        frame,
        1
    )


    # ========================================================
    # 8. GRAYSCALE IMAGE
    # ========================================================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # ========================================================
    # 9. MOVEMENT DETECTION
    # ========================================================

    movement_detected = False
    movement_pixels = 0

    if previous_gray is not None:

        difference = cv2.absdiff(
            previous_gray,
            gray
        )

        # Reduce camera noise
        difference = cv2.GaussianBlur(
            difference,
            (5, 5),
            0
        )

        _, movement_mask = cv2.threshold(
            difference,
            25,
            255,
            cv2.THRESH_BINARY
        )

        movement_pixels = cv2.countNonZero(
            movement_mask
        )

        if movement_pixels > MOVEMENT_THRESHOLD:

            movement_detected = True


    previous_gray = gray.copy()


    # ========================================================
    # 10. YOLO HUMAN DETECTION
    # ========================================================

    results = model(
        frame,
        conf=0.25,
        classes=[0],
        verbose=False
    )


    people_count = 0
    best_confidence = 0.0


    for result in results:

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )


            # Class 0 = person
            if class_id == 0:

                people_count += 1


                if confidence > best_confidence:

                    best_confidence = confidence


                # Coordinates
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                # Draw red bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )


                # Label
                label = (
                    f"SURVIVOR "
                    f"{confidence * 100:.0f}%"
                )


                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 25)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 0, 255),
                    2
                )


    # ========================================================
    # 11. THERMAL-STYLE FILTER
    # ========================================================

    enhanced_gray = cv2.equalizeHist(
        gray
    )


    thermal = cv2.applyColorMap(
        enhanced_gray,
        cv2.COLORMAP_JET
    )


    # ========================================================
    # 12. DRAW PERSON BOXES ON THERMAL VIEW
    # ========================================================

    for result in results:

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )


            if class_id == 0:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )


                cv2.rectangle(
                    thermal,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    3
                )


                cv2.putText(
                    thermal,
                    f"SURVIVOR {confidence * 100:.0f}%",
                    (x1, max(y1 - 10, 25)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 255),
                    2
                )


    # ========================================================
    # 13. AUDIO DETECTION
    # ========================================================

    audio_spike = False

    if audio_supported:

        if (
            audio_level > AUDIO_RMS_THRESHOLD
            or
            audio_peak > AUDIO_PEAK_THRESHOLD
        ):

            audio_spike = True


    # ========================================================
    # 14. SURVIVOR ALERT
    # ========================================================

    survivor_detected = people_count > 0


    confirmed_alert = False


    if survivor_detected:

        if alert_start_time is None:

            alert_start_time = time.time()


        elapsed_time = (
            time.time()
            -
            alert_start_time
        )


        if elapsed_time >= CONFIRMATION_TIME:

            confirmed_alert = True


    else:

        alert_start_time = None


    # ========================================================
    # 15. INFORMATION PANEL
    # ========================================================

    overlay = thermal.copy()


    cv2.rectangle(
        overlay,
        (0, 0),
        (450, 170),
        (20, 20, 20),
        -1
    )


    thermal = cv2.addWeighted(
        overlay,
        0.85,
        thermal,
        0.15,
        0
    )


    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    cv2.putText(
        thermal,
        "AEROGUARD AI VISION",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 242, 254),
        2
    )


    # --------------------------------------------------------
    # Survivor status
    # --------------------------------------------------------

    if people_count > 0:

        survivor_text = (
            f"SURVIVORS: "
            f"{people_count} DETECTED"
        )

        survivor_color = (0, 255, 0)

    else:

        survivor_text = (
            "SURVIVORS: SEARCHING..."
        )

        survivor_color = (255, 255, 255)


    cv2.putText(
        thermal,
        survivor_text,
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        survivor_color,
        2
    )


    # --------------------------------------------------------
    # Movement status
    # --------------------------------------------------------

    if movement_detected:

        movement_text = "MOTION: DETECTED"
        movement_color = (0, 255, 0)

    else:

        movement_text = "MOTION: STABLE"
        movement_color = (255, 255, 255)


    cv2.putText(
        thermal,
        movement_text,
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        movement_color,
        2
    )


    # --------------------------------------------------------
    # Audio status
    # --------------------------------------------------------

    if not audio_supported:

        audio_text = "AUDIO: NOT AVAILABLE"
        audio_color = (0, 0, 255)

    elif audio_spike:

        audio_text = "AUDIO: SPIKE DETECTED"
        audio_color = (0, 255, 255)

    else:

        audio_text = "AUDIO: MONITORING"
        audio_color = (255, 255, 255)


    cv2.putText(
        thermal,
        audio_text,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        audio_color,
        2
    )


    # --------------------------------------------------------
    # People count
    # --------------------------------------------------------

    cv2.putText(
        thermal,
        f"PEOPLE COUNT: {people_count}",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    # ========================================================
    # 16. SURVIVOR ALERT
    # ========================================================

    if confirmed_alert:

        cv2.rectangle(
            thermal,
            (80, 200),
            (880, 270),
            (0, 0, 255),
            -1
        )


        cv2.putText(
            thermal,
            "SURVIVOR LOCATED!",
            (260, 245),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            3
          )




    # ========================================================
    # 17. SHOW THERMAL WINDOW
    # ========================================================

    cv2.imshow(
        "AeroGuard - Thermal Rescue Vision",
        thermal
    )


    # ========================================================
    # 18. QUIT WITH Q
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


# ============================================================
# 19. CLEANUP
# ============================================================

print()
print("Stopping AeroGuard...")


cap.release()

cv2.destroyAllWindows()


if audio_stream is not None:

    try:

        audio_stream.stop()
        audio_stream.close()

    except Exception:
        pass


print("AeroGuard stopped successfully.")
print("==========================================")
