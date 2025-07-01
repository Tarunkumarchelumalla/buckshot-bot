import pyautogui
import cv2
import numpy as np
import pygetwindow as gw
from ultralytics import YOLO
import time
from pynput.mouse import Controller, Button

class BuckshotRouletteBot:
    def __init__(self, model_path: str, window_title: str = "Buckshot Roulette"):
        self.model = YOLO(model_path)
        self.mouse = Controller()
        self.window_title = window_title

    def focus_window(self):
        try:
            windows = gw.getWindowsWithTitle(self.window_title)
            if windows:
                windows[0].restore()
                windows[0].activate()
                time.sleep(0.2)
            else:
                print("❌ Game window not found!")
        except Exception as e:
            print(f"⚠️ Could not focus window: {e}")

    def click(self, x, y):
        try:
            self.mouse.position = (x, y)
            time.sleep(0.05)
            self.mouse.press(Button.left)
            time.sleep(0.05)
            self.mouse.release(Button.left)
        except Exception as e:
            print(f"❌ Click failed: {e}")

    def get_window_region(self):
        try:
            windows = gw.getWindowsWithTitle(self.window_title)
            if not windows:
                print("❌ Game window not found!")
                return None
            w = windows[0]
            return (w.left, w.top, w.width, w.height)
        except Exception as e:
            print(f"⚠️ Error getting window region: {e}")
            return None

    def detect_objects(self, region):
        try:
            x, y, w, h = region
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            results = self.model.predict(source=frame, conf=0.4, verbose=False)[0]
            objects = []

            for box in results.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                objects.append({"label": label, "confidence": round(conf, 2), "bbox": [x1, y1, x2, y2]})

            return objects
        except Exception as e:
            print(f"❌ Detection failed: {e}")
            return []

    def click_fixed_position(self, pos, region):
        try:
            x, y, w, h = region
            if pos == "center":
                cx, cy = x + w // 2, y + int(h * 0.45)
            elif pos == "top":
                cx, cy = x + w // 2, y + int(h * 0.2)
            elif pos == "bottom":
                cx, cy = x + w // 2, y + int(h * 0.8)
            else:
                print(f"⚠️ Unknown position '{pos}'")
                return
            print(f"🖱️ Clicking {pos} at ({cx}, {cy})")
            self.click(cx, cy)
        except Exception as e:
            print(f"❌ click_fixed_position error: {e}")

    def click_on_object(self, label, region):
        def closeness_to_bottom(obj):
            x1, y1, x2, y2 = obj["bbox"]
            return -((y1 + y2) // 2)

        objects = self.detect_objects(region)
        matches = [obj for obj in objects if obj["label"].lower() == label.lower()]
        if not matches:
            print(f"⚠️ '{label}' not found.")
            return

        chosen = max(matches, key=closeness_to_bottom)
        x1, y1, x2, y2 = chosen["bbox"]
        cx = region[0] + (x1 + x2) // 2
        cy = region[1] + (y1 + y2) // 2

        if label.lower() == "inventorybox":
            cy = region[1] + y1 + int(0.85 * (y2 - y1))
            print(f"🖱️ Clicking inventorybox at ({cx}, {cy})")
        else:
            print(f"🖱️ Clicking '{label}' at ({cx}, {cy})")

        self.click(cx, cy)

        # Try closing inventory
        if label.lower() == "inventorybox":
            print("📦 Trying to close inventory...")
            timeout = time.time() + 10
            while time.time() < timeout:
                time.sleep(0.4)
                new_objs = self.detect_objects(region)
                empty = [o for o in new_objs if o["label"].lower() == "emptyspace"]
                if empty:
                    closest = max(empty, key=closeness_to_bottom)
                    ex1, ey1, ex2, ey2 = closest["bbox"]
                    ecx = region[0] + (ex1 + ex2) // 2
                    ecy = region[1] + (ey1 + ey2) // 2
                    print(f"🖱️ Clicking emptyspace at ({ecx}, {ecy})")
                    self.click(ecx, ecy)
                    self.click_on_object("inventorybox", region)
                else:
                    print("⚠️ No emptyspace, clicking corner.")
                    self.click(region[0] + 20, region[1] + 20)

                inv_check = self.detect_objects(region)
                if not any(o["label"].lower() == "inventorybox" for o in inv_check):
                    print("✅ Inventory closed.")
                    return
            print("❌ Inventory did not close.")

    def run_command(self, command: str):
        """
        Execute a single command like 'shoot dealer', 'pick item', etc.
        """
        region = self.get_window_region()
        if not region:
            print("❌ Could not find game window.")
            return

        self.focus_window()
        command = command.strip().lower()

        if command == "shoot":
            self.click_fixed_position("center", region)
        elif command == "enemy":
            self.click_fixed_position("top", region)
        elif command in ["myself", "shoot me"]:
            self.click_fixed_position("bottom", region)
        elif command.startswith("pick "):
            label = command.replace("pick ", "").strip()
            self.click_on_object(label, region)
        else:
            print(f"⚠️ Unknown command: '{command}'")
