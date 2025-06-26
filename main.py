import pyautogui
import pytesseract
import time
from PIL import Image
import cv2
import numpy as np
import pygetwindow as gw
import os

# Set this manually if Tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load templates once
TEMPLATE_FOLDER = "templates"
TEMPLATES = {f.split('.')[0]: cv2.imread(os.path.join(TEMPLATE_FOLDER, f), 0) 
             for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(('.png', '.jpg'))}

def get_window_region(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if not window.isMinimized:
            return (window.left, window.top, window.width, window.height)
    except IndexError:
        print(f"Window '{window_title}' not found.")
    return None

def get_text_from_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    text = pytesseract.image_to_string(screenshot_cv)
    print("📝 Extracted Text:", text.strip())
    return text.strip(), screenshot_cv

def match_items_on_screen(screen_gray, base_x, base_y):
    found_items = []
    for name, template in TEMPLATES.items():
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust this if needed
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            found_items.append((name, pt))
            print(f"🔍 Found item: {name} at {pt}")
            # Optional: Click on item
            # pyautogui.click(base_x + pt[0], base_y + pt[1])
    return found_items

def perform_action_based_on_text(text, base_x, base_y):
    if "Your Turn" in text:
        print("🎯 Action: Your Turn — clicking fire button")
        pyautogui.click(x=base_x + 200, y=base_y + 300)
    elif "Pass" in text:
        print("🎯 Action: Pass — clicking pass button")
        pyautogui.click(x=base_x + 400, y=base_y + 300)
    else:
        print("🚫 No matching text for action.")

# Set your game window title
window_title = "Buckshot Roulette"

while True:
    region = get_window_region(window_title)
    if region:
        x, y, w, h = region
        text, screenshot_color = get_text_from_screen((x, y, w, h))

        # OCR-based decisions
        perform_action_based_on_text(text, x, y)

        # Template matching on grayscale version
        screenshot_gray = cv2.cvtColor(screenshot_color, cv2.COLOR_BGR2GRAY)
        match_items_on_screen(screenshot_gray, x, y)

    time.sleep(2)
