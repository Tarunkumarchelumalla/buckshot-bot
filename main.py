import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
from ultralytics import YOLO
from collections import Counter
import time
import keyboard
from pynput.mouse import Controller, Button

# Load YOLO model
model = YOLO("runs/detect/train9_without_compression/weights/best.pt")
mouse = Controller()

def focus_window(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            windows[0].restore()
            windows[0].activate()
            time.sleep(0.2)
        else:
            print("❌ Game window not found!")
    except Exception as e:
        print(f"⚠️ Could not focus window: {e}")

def click_with_pynput(x, y):
    try:
        mouse.position = (x, y)
        time.sleep(0.05)
        mouse.press(Button.left)
        time.sleep(0.05)
        mouse.release(Button.left)
    except Exception as e:
        print(f"❌ Click failed: {e}")

def get_window_region(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            print("❌ Game window not found!")
            return None
        w = windows[0]
        return (w.left, w.top, w.width, w.height)
    except Exception as e:
        print(f"⚠️ Error getting window region: {e}")
        return None

def detect_objects_in_region(region):
    try:
        x, y, w, h = region
        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        results = model.predict(source=frame, conf=0.4, verbose=False)[0]

        objects = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            objects.append({
                "label": label,
                "confidence": round(conf, 2),
                "bbox": [x1, y1, x2, y2]
            })

        cv2.imshow("Detection Window", frame)
        cv2.waitKey(1)
        return objects
    except Exception as e:
        print(f"❌ Detection failed: {e}")
        return []

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

def click_on_object(label_to_click, region):
    x, y, w, h = region
    print(f"🔍 Detecting to find '{label_to_click}'...")
    objects = detect_objects_in_region(region)

    # Match item by label
    matching_objects = [obj for obj in objects if obj["label"].lower() == label_to_click.lower()]
    if not matching_objects:
        print(f"⚠️ '{label_to_click}' not found in detected objects.")
        return

    # Choose object closest to bottom
    def closeness_to_bottom(obj):
        x1, y1, x2, y2 = obj["bbox"]
        obj_center_y = (y1 + y2) // 2
        return -obj_center_y  # More positive means lower on screen

    closest_object = max(matching_objects, key=closeness_to_bottom)
    x1, y1, x2, y2 = closest_object["bbox"]
    obj_center_x = (x1 + x2) // 2
    obj_center_y = (y1 + y2) // 2

    abs_x = x + obj_center_x
    abs_y = y + obj_center_y

    if label_to_click.lower() == "inventorybox":
        abs_y = y + y1 + int(0.85 * (y2 - y1))
        print(f"🖱️ Picking 'inventorybox' near bottom at ({abs_x}, {abs_y})")
    else:
        print(f"🖱️ Picking '{label_to_click}' at ({abs_x}, {abs_y})")

    click_with_pynput(abs_x, abs_y)

    # Handle inventorybox dismiss logic
    if label_to_click.lower() == "inventorybox":
        print("📦 Inventory opened — will try to dismiss it by clicking on 'emptyspace'")
        timeout = time.time() + 10

        while time.time() < timeout:
            time.sleep(0.4)
            new_objects = detect_objects_in_region(region)
            emptyspaces = [o for o in new_objects if o["label"].lower() == "emptyspace"]

            if emptyspaces:
                # Choose emptyspace closest to bottom
                closest_empty = max(emptyspaces, key=closeness_to_bottom)
                ex1, ey1, ex2, ey2 = closest_empty["bbox"]
                ecx = x + (ex1 + ex2) // 2
                ecy = y + (ey1 + ey2) // 2
                print(f"🖱️ Clicking emptyspace at ({ecx}, {ecy})")
                click_with_pynput(ecx, ecy)
            else:
                print("⚠️ No 'emptyspace'. Clicking top-left corner.")
                click_with_pynput(x + 20, y + 20)

            inv_check = detect_objects_in_region(region)
            if not any(o["label"].lower() == "inventorybox" for o in inv_check):
                print("✅ Inventory closed.")
                return

        print("❌ Gave up trying to close inventory.")

def click_fixed_position(position, region):
    try:
        x, y, w, h = region
        if position == "center":
            cx = x + w // 2
            cy = y + int(h * 0.45)
        elif position == "top":
            cx = x + w // 2
            cy = y + int(h * 0.2)
        elif position == "bottom":
            cx = x + w // 2
            cy = y + int(h * 0.8)
        else:
            print(f"⚠️ Unknown position '{position}'")
            return
        print(f"🖱️ Clicking {position} at ({cx}, {cy})")
        click_with_pynput(cx, cy)
    except Exception as e:
        print(f"❌ click_fixed_position error: {e}")

# -----------------------------
# MAIN LOOP
# -----------------------------
if __name__ == "__main__":
    window_title = "Buckshot Roulette"
    print("🎮 Watching for game window... Press 'Q' to quit.")

    while True:
        try:
            if keyboard.is_pressed('q'):
                print("👋 Exiting...")
                cv2.destroyAllWindows()
                break

            region = get_window_region(window_title)
            if region:
                focus_window(window_title)
                latest_objects = detect_objects_in_region(region)
                print_detections(latest_objects)

                print("\n🗣️ Type a command (shoot / shoot dealer / shoot myself / pick <item>):")
                command = input("> ").strip().lower()

                if command == "shoot":
                    click_fixed_position("center", region)
                elif command == "shoot dealer":
                    click_fixed_position("top", region)
                elif command in ["shoot myself", "shoot me"]:
                    click_fixed_position("bottom", region)
                elif command.startswith("pick "):
                    item = command.replace("pick ", "").strip()
                    click_on_object(item, region)
            else:
                print("⌛ Retrying in 2 seconds...")

            time.sleep(2)
        except Exception as e:
            print(f"💥 Main loop error: {e}")
