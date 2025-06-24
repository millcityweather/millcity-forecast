import os
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Load environment variable for Dropbox
DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")

# Constants
LAT = 42.6465
LON = -71.3121
TIMEZONE = "America/New_York"
TEMPLATE_PATH = "sunrisesunsettemplate.png"
FONT_PATH = "assets/fonts/Helvetica Neue LT Std 83 Heavy Extended.otf"
OUTPUT_PATH = "sunrise_graphic.png"
DROPBOX_DEST_PATH = "/sunrise_graphic.png"

# Fetch sunrise/sunset data
def get_sun_times():
    url = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0"
    response = requests.get(url)
    data = response.json()['results']

    sunrise_utc = datetime.fromisoformat(data['sunrise'])
    sunset_utc = datetime.fromisoformat(data['sunset'])

    sunrise_local = sunrise_utc.astimezone().strftime("%-I:%M %p")
    sunset_local = sunset_utc.astimezone().strftime("%-I:%M %p")

    return sunrise_local, sunset_local

# Generate graphic
def create_graphic(sunrise_time, sunset_time):
    image = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 92)

    # Aligned x position for both times
    x = 715
    draw.text((x, 395), sunrise_time, font=font, fill="gold")
    draw.text((x, 660), sunset_time, font=font, fill="gold")

    image.save(OUTPUT_PATH)
    print("✅ Image saved:", OUTPUT_PATH)

# Upload to Dropbox
def upload_to_dropbox(local_path, dropbox_path):
    import dropbox
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    print("✅ Uploaded to Dropbox:", dropbox_path)

# Main
if __name__ == "__main__":
    sunrise, sunset = get_sun_times()
    create_graphic(sunrise, sunset)
    upload_to_dropbox(OUTPUT_PATH, DROPBOX_DEST_PATH)



