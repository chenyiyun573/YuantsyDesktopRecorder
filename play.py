import os
import csv
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import pygame

# Directory paths
log_dir = './desktop_log'
log_file = os.path.join(log_dir, 'event_log.csv')
screenshot_path = os.path.join(log_dir, 'screenshot')

# Font settings
font_path = "arial.ttf"
font_size = 20

def read_event_log():
    events = []
    with open(log_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append(row)
    return events

def draw_text(image, text, position):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill="white")
    return image

def draw_mouse_icon(image, position):
    draw = ImageDraw.Draw(image)
    x, y = position
    draw.ellipse((x-10, y-10, x+10, y+10), outline="red", width=3)
    return image

def annotate_image(image_path, event):
    img = Image.open(image_path).convert("RGBA")
    if event['Event Type'] == 'Key Press':
        img = draw_text(img, event['Details'], (10, 10))
    elif event['Event Type'].startswith('Mouse'):
        pos = event['Details'].split('at ')[1].split(')')[0].strip('()').split(',')
        mouse_pos = (int(pos[0]), int(pos[1]))
        img = draw_mouse_icon(img, mouse_pos)
    return img

def play_events():
    events = read_event_log()
    
    # Initialize pygame
    pygame.init()
    
    # Get the display info
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    
    last_screenshot = events[0]['Screenshot']
    previous_timestamp = None

    for event in events:
        timestamp = datetime.strptime(event['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        screenshot = event['Screenshot']
        
        if previous_timestamp:
            duration = (timestamp - previous_timestamp).total_seconds()
        else:
            duration = 1  # Default duration for the first frame

        if screenshot:
            last_screenshot = screenshot

        img = annotate_image(last_screenshot, event)
        img = img.convert("RGB")
        
        # Scale the image to fit the screen
        img = img.resize((screen_width, screen_height), Image.LANCZOS)
        mode = img.mode
        size = img.size
        data = img.tobytes()

        # Display the image
        py_img = pygame.image.fromstring(data, size, mode)
        screen.blit(py_img, (0, 0))
        pygame.display.flip()

        # Pause for the duration
        time.sleep(duration)

        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        previous_timestamp = timestamp
    
    # Keep the last frame displayed until the user closes the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    play_events()
