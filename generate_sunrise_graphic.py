from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests

# === File paths ===
template_path = "template.png"
output_path = "sunrise_graphic.png"
font_path = "assets/fonts/Helvetica Neue LT Std 83 Heavy Extended.otf"
font_size = 88

# === Load font ===
font = ImageFont.truetype(font_path, font_size)

# === Open image and draw ===
image = Image.open(template_path)
draw = ImageDraw.Draw(image)

# === Get sunrise/sunset data ===
# Using static fallback times — you can replace this with live data later
sunrise_time = "5:09 AM"
sunset_time = "8:27 PM"

# === Calculate daylight duration ===
def get_daylight_length(start_str, end_str):
    fmt = "%I:%M %p"
    try:
        t1 = datetime.strptime(start_str, fmt)
        t2 = datetime.strptime(end_str, fmt)
        duration = datetime.combine(datetime.min, t2.time()) - datetime.combine(datetime.min, t1.time())
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    except Exception:
        return "—"

daylight = get_daylight_length(sunrise_time, sunset_time)

# === Draw the text (adjust these positions to match your template)
draw.text((160, 870), sunrise_time, font=font, fill="white")
draw.text((720, 870), sunset_time, font=font, fill="white")
draw.text((1290, 870), daylight, font=font, fill="white")

# === Save the output ===
image.save(output_path)
print("✅ Sunrise graphic saved as:", output_path)

