import cv2
import numpy as np

# Video Parameters
WIDTH, HEIGHT = 720, 1280  # Vertical 9:16 aspect ratio (Drone View)
FPS = 30
DURATION_SEC = 10
TOTAL_FRAMES = FPS * DURATION_SEC
OUTPUT_FILE = "real_thermal_drone.mp4"

# Set up Video Writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

# Generate Synthetic Forest & Terrain Base Background
np.random.seed(42)
terrain_base = np.random.normal(60, 15, (HEIGHT, WIDTH)).astype(np.float32)

# Create Organic Tree Canopy Structures (Fractal/Noise Texture)
trees = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
for _ in range(150):
    tx, ty = np.random.randint(50, WIDTH - 50), np.random.randint(50, HEIGHT - 50)
    radius = np.random.randint(30, 90)
    cv2.circle(trees, (tx, ty), radius, (np.random.randint(120, 180)), -1)

trees = cv2.GaussianBlur(trees, (81, 81), 0)
background = cv2.addWeighted(terrain_base, 0.6, trees, 0.4, 0)

# Define Moving Thermal Human Targets (Bright Glowing Figures)
targets = [
    {"x": 300, "y": 900, "vx": 0.5, "vy": -1.2, "size": 6},
    {"x": 320, "y": 920, "vx": 0.6, "vy": -1.0, "size": 5},
    {"x": 280, "y": 940, "vx": 0.4, "vy": -1.3, "size": 6},
    {"x": 450, "y": 700, "vx": -0.8, "vy": -0.4, "size": 5},
    {"x": 200, "y": 400, "vx": 0.3, "vy": 0.8, "size": 6},
    {"x": 550, "y": 300, "vx": -0.5, "vy": 0.5, "size": 5},
]

print("🎥 Generating Realistic Aerial Thermal Video...")

# Camera Panning Simulation
cam_x, cam_y = 0.0, 0.0

for frame_idx in range(TOTAL_FRAMES):
    # Camera slow drift
    cam_x += 0.3
    cam_y += 0.5
    
    # Base thermal canvas (Grayscale White Hot)
    frame_thermal = background.copy()
    
    # Add Moving Targets (Glowing Thermal Signatures)
    target_layer = np.zeros((HEIGHT, WIDTH), dtype=np.float32)
    
    for t in targets:
        t["x"] += t["vx"] + np.random.uniform(-0.3, 0.3)
        t["y"] += t["vy"] + np.random.uniform(-0.3, 0.3)
        
        tx, ty = int(t["x"]), int(t["y"])
        
        if 20 < tx < WIDTH - 20 and 20 < ty < HEIGHT - 20:
            # High intensity white thermal core (Body heat)
            cv2.circle(target_layer, (tx, ty), t["size"], 255.0, -1)
            # Thermal bloom effect
            cv2.circle(target_layer, (tx, ty), t["size"] * 3, 180.0, -1)

    # Soften thermal glow to look like real optics
    target_layer = cv2.GaussianBlur(target_layer, (15, 15), 0)
    
    # Combine Terrain + Targets
    combined = cv2.addWeighted(frame_thermal, 0.7, target_layer, 0.9, 0)
    
    # Apply Sensor Noise & Grain
    noise = np.random.normal(0, 8, (HEIGHT, WIDTH)).astype(np.float32)
    combined = np.clip(combined + noise, 0, 255).astype(np.uint8)

    # Convert to 3-channel grayscale BGR video frame
    frame_bgr = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)

    # Alternate: Enable Real False-Color Thermal (Ironbow Mode) after frame 180
    if frame_idx > 180:
        frame_bgr = cv2.applyColorMap(combined, cv2.COLORMAP_JET)

    out.write(frame_bgr)

out.release()
print("✅ Video saved successfully as 'real_thermal_drone.mp4'!")
