
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Load template and font
template = Image.open("template.png").convert("RGBA")
draw = ImageDraw.Draw(template)
font = ImageFont.truetype("Helvetica Neue LT Std 83 Heavy Extended.otf", 108)
yellow = (255, 215, 0)

# Get sunrise/sunset times
lat, lon = 42.6457, -71.3162
url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date=today&formatted=0"
r = requests.get(url)
data = r.json()["results"]

def to_local(utc):
    t = datetime.fromisoformat(utc.replace("Z", "+00:00")) - timedelta(hours=4)
    return t.strftime("%-I:%M %p")

sunrise = to_local(data["sunrise"])
sunset = to_local(data["sunset"])

# Draw times on image
draw.text((735, 410), sunrise, font=font, fill=yellow)
draw.text((735, 665), sunset, font=font, fill=yellow)

# Save output
template.save("sunrise.png")
