import os
import csv
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip

# Directory paths
log_dir = './desktop_log'
log_file = os.path.join(log_dir, 'event_log.csv')
screenshot_path = os.path.join(log_dir, 'screenshot')

# Font settings
font_path = "arial.ttf"  # Make sure the font file is available or use another font
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

def create_video_from_screenshots():
    events = read_event_log()
    
    clips = []
    previous_timestamp = None
    last_screenshot = None
    
    for event in events:
        timestamp = datetime.strptime(event['Timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        screenshot = event['Screenshot']
        event_type = event['Event Type']
        details = event['Details']
        
        if previous_timestamp:
            duration = (timestamp - previous_timestamp).total_seconds()
        else:
            duration = 1  # Default duration for the first frame

        if screenshot:
            last_screenshot = screenshot

        if last_screenshot:
            img = Image.open(last_screenshot).convert("RGBA")
            if event_type == 'Key Press':
                img = draw_text(img, details, (10, 10))
            if event_type.startswith('Mouse'):
                pos = details.split('at ')[1].split(')')[0].strip('()').split(',')
                mouse_pos = (int(pos[0]), int(pos[1]))
                img = draw_mouse_icon(img, mouse_pos)

            annotated_img_path = os.path.join(screenshot_path, f"annotated_{os.path.basename(last_screenshot)}")
            img.save(annotated_img_path)

            base_clip = ImageClip(annotated_img_path).set_duration(duration)
            overlay_clips = []

            if event_type == 'Key Press':
                text_clip = ImageClip(annotated_img_path).set_duration(0.5)
                overlay_clips.append(text_clip)

            if event_type.startswith('Mouse'):
                mouse_clip = ImageClip(annotated_img_path).set_duration(0.5)
                overlay_clips.append(mouse_clip)

            if overlay_clips:
                annotated_clip = CompositeVideoClip([base_clip] + overlay_clips)
            else:
                annotated_clip = base_clip

            clips.append(annotated_clip)
        
        previous_timestamp = timestamp

    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(os.path.join(log_dir, "output_video.mp4"), codec="libx264", fps=24)

if __name__ == "__main__":
    create_video_from_screenshots()
