from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import dropbox

# === Dropbox Settings ===
DROPBOX_ACCESS_TOKEN = "YOUR_DROPBOX_ACCESS_TOKEN"
DROPBOX_DEST_PATH = "/sunrise_graphic.png"

# === Image & Font Settings ===
TEMPLATE_PATH = "template.png"
OUTPUT_PATH = "sunrise_graphic.png"
FONT_PATH = "assets/fonts/Helvetica Neue LT Std 83 Heavy Extended.otf"
FONT_SIZE = 88

# === Get Sunrise/Sunset Times (Live API) ===
def get_sunrise_sunset():
    url = "https://api.sunrise-sunset.org/json?lat=42.6334&lng=-71.3162&formatted=0"
    try:
        response = requests.get(url)
        data = response.json()["results"]
        sunrise_utc = datetime.fromisoformat(data["sunrise"])
        sunset_utc = datetime.fromisoformat(data["sunset"])
        local_timezone = datetime.now().astimezone().tzinfo
        sunrise = sunrise_utc.astimezone(local_timezone).strftime("%-I:%M %p")
        sunset = sunset_utc.astimezone(local_timezone).strftime("%-I:%M %p")
        return sunrise, sunset
    except:
        return "—", "—"

# === Daylight Duration ===
def get_daylight_length(start_str, end_str):
    fmt = "%I:%M %p"
    try:
        t1 = datetime.strptime(start_str, fmt)
        t2 = datetime.strptime(end_str, fmt)
        duration = datetime.combine(datetime.min, t2.time()) - datetime.combine(datetime.min, t1.time())
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    except:
        return "—"

# === Upload to Dropbox ===
def upload_to_dropbox(local_path, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    print("✅ Uploaded to Dropbox:", dropbox_path)

# === Main Process ===
def main():
    sunrise, sunset = get_sunrise_sunset()
    daylight = get_daylight_length(sunrise, sunset)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    image = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(image)

    # Draw sunrise, sunset, daylight (adjust positions if needed)
    draw.text((160, 870), sunrise, font=font, fill="white")
    draw.text((720, 870), sunset, font=font, fill="white")
    draw.text((1290, 870), daylight, font=font, fill="white")

    # Save image
    image.save(OUTPUT_PATH)
    print("✅ Image saved:", OUTPUT_PATH)

    # Upload to Dropbox
    upload_to_dropbox(OUTPUT_PATH, DROPBOX_DEST_PATH)

if __name__ == "__main__":
    main()


