import os
import csv
import time
from datetime import datetime
from pynput import mouse, keyboard
from PIL import ImageGrab
from threading import Thread

# Ensure the directory exists
log_dir = './desktop_log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Define the output CSV file and screenshot directory
log_file = os.path.join(log_dir, 'event_log.csv')
screenshot_path = os.path.join(log_dir, 'screenshot')

# Ensure the screenshot directory exists
if not os.path.exists(screenshot_path):
    os.makedirs(screenshot_path)

# Open the CSV file for writing
with open(log_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Event Type', 'Details', 'Screenshot'])

    last_times = {
        'mouse_click': 0,
        'mouse_scroll': 0,
        'key_press': 0,
        'mouse_move': 0
    }
    min_interval_seconds = 0.3  # Minimum interval between screenshots for each event

    def take_screenshot(event_time, event_type):
        filename = f"{event_time.strftime('%Y-%m-%d %H-%M-%S.%f')[:-3]}.png"
        full_path = os.path.join(screenshot_path, filename)
        ImageGrab.grab().save(full_path)
        print(f"[DEBUG] Screenshot taken for {event_type} at {full_path}")
        return full_path

    def should_take_screenshot(event_type):
        current_time = time.time()
        if current_time - last_times[event_type] >= min_interval_seconds:
            last_times[event_type] = current_time
            return True
        return False

    def on_click(x, y, button, pressed):
        event_time = datetime.now()
        timestamp = event_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        event_description = f"Mouse {'clicked' if pressed else 'released'} at ({x}, {y}) with {button}"
        screenshot = take_screenshot(event_time, 'mouse_click') if pressed and should_take_screenshot('mouse_click') else ''
        writer.writerow([timestamp, 'Mouse Click', event_description, screenshot])
        file.flush()
        print(f"[DEBUG] {event_description}")

    def on_scroll(x, y, dx, dy):
        event_time = datetime.now()
        timestamp = event_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        event_description = f"Mouse scrolled at ({x}, {y}) by ({dx}, {dy})"
        screenshot = take_screenshot(event_time, 'mouse_scroll') if should_take_screenshot('mouse_scroll') else ''
        writer.writerow([timestamp, 'Mouse Scroll', event_description, screenshot])
        file.flush()
        print(f"[DEBUG] {event_description}")

    def on_move(x, y):
        event_time = datetime.now()
        timestamp = event_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        event_description = f"Mouse moved to ({x}, {y})"
        screenshot = take_screenshot(event_time, 'mouse_move') if should_take_screenshot('mouse_move') else ''
        writer.writerow([timestamp, 'Mouse Move', event_description, screenshot])
        file.flush()
        print(f"[DEBUG] {event_description}")

    def on_press(key):
        event_time = datetime.now()
        timestamp = event_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        try:
            event_description = f"Key {key.char} pressed"
        except AttributeError:
            event_description = f"Special key {key} pressed"
        screenshot = take_screenshot(event_time, 'key_press') if should_take_screenshot('key_press') else ''
        writer.writerow([timestamp, 'Key Press', event_description, screenshot])
        file.flush()
        print(f"[DEBUG] {event_description}")

    def periodic_screenshot():
        while True:
            time.sleep(30)
            take_screenshot(datetime.now(), 'periodic')

    # Start the periodic screenshot in a separate thread
    thread = Thread(target=periodic_screenshot)
    thread.start()

    # Set up listeners
    # Yiyun: the mouse move is too frequent, so I commented it out
    # with mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as mouse_listener:
    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        with keyboard.Listener(on_press=on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()

thread.join()
