from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests

# === Load the template image ===
template_path = "template.png"  # Make sure this exists
output_path = "sunrise_graphic.png"

# === Load font ===
font_path = "assets/fonts/HelveticaNeueLTStd-HvEx.otf"
font_size = 88
font = ImageFont.truetype(font_path, font_size)

# === Fetch data from NWS API ===
response = requests.get("https://api.weather.gov/gridpoints/BOX/59,84/forecast")
data = response.json()

# === Extract sunrise, sunset from today's period ===
today = data["properties"]["periods"][0]
sunrise = today.get("sunrise", "5:09 AM")  # fallback if missing
sunset = today.get("sunset", "8:27 PM")    # fallback if missing

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

daylight = get_daylight_length(sunrise, sunset)

# === Open image and draw text ===
image = Image.open(template_path)
draw = ImageDraw.Draw(image)

# === Positioning — adjust as needed ===
draw.text((160, 870), sunrise, font=font, fill="white")      # Sunrise
draw.text((720, 870), sunset, font=font, fill="white")       # Sunset
draw.text((1290, 870), daylight, font=font, fill="white")    # Daylight duration

# === Save result ===
image.save(output_path)
print("Sunrise graphic generated:", output_path)
