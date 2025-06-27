import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
from ultralytics import YOLO
from collections import Counter
import time

# Load your trained YOLOv8 model
model = YOLO("runs/detect/train8/weights/best.pt")  # Update the path if needed

def get_window_region(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        print("❌ Game window not found!")
        return None
    w = windows[0]
    return (w.left, w.top, w.width, w.height)

def detect_objects_in_region(region):
    x, y, w, h = region
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    results = model.predict(source=frame, conf=0.4, verbose=False)[0]
    print({results})
    objects = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        objects.append({
            "label": label,
            "confidence": round(conf, 2),
            "bbox": [x1, y1, x2, y2]
        })
    return objects

def print_detections(objects):
    if not objects:
        print("🔍 No objects detected.")
        return

    print("\n📦 Detected Objects:")
    for obj in objects:
        print(f"  - {obj['label']} | Confidence: {obj['confidence']} | Box: {obj['bbox']}")

    counts = dict(Counter([obj["label"] for obj in objects]))
    print("\n🔢 Object Counts:")
    for label, count in counts.items():
        print(f"  - {label}: {count}")

if __name__ == "__main__":
    window_title = "Buckshot Roulette"
    print("🎮 Watching for game window...")
    while True:
        region = get_window_region(window_title)
        if region:
            objects = detect_objects_in_region(region)
            print_detections(objects)
        else:
            print("⌛ Retrying in 2 seconds...")
        time.sleep(2)
