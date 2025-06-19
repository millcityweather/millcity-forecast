import requests
from PIL import Image, ImageDraw, ImageFont
import datetime

# ---- Load base image ----
template_path = "weathercam_template.png"
output_path = "weathercam.png"
image = Image.open(template_path).convert("RGBA")
draw = ImageDraw.Draw(image)

# ---- Font config ----
font_path = "Helvetica Neue LT Std 83 Heavy Extended.otf"
font = ImageFont.truetype(font_path, 90)

# ---- Convert helper ----
def kelvin_to_f(k):
    return round((k - 273.15) * 9 / 5 + 32) if k is not None else "—"

def meters_to_miles(m):
    return round(m / 1609.344, 1) if m else "—"

def pa_to_inhg(pa):
    return round(pa * 0.0002953, 2) if pa else "—"

# ---- Fetch NWS data ----
station = "KLWM"  # Lawrence Municipal Airport, closest to Lowell
url = f"https://api.weather.gov/stations/{station}/observations/latest"
headers = {"User-Agent": "millcityweather.com"}
res = requests.get(url, headers=headers)
data = res.json()["properties"]

# ---- Parse + convert values ----
temp_f = kelvin_to_f(data["temperature"]["value"])
dew_f = kelvin_to_f(data["dewpoint"]["value"])
vis_miles = meters_to_miles(data["visibility"]["value"])
pressure_in = pa_to_inhg(data["barometricPressure"]["value"])
wind_spd = round(data["windSpeed"]["value"] * 0.621371) if data["windSpeed"]["value"] else "—"
wind_dir = data["windDirection"]["value"] or "—"
wind = f"{wind_dir} {wind_spd}"

# ---- Draw text onto image (adjust positions as needed) ----
draw.text((90, 320), f"{temp_f}°", font=font, fill="black")         # Temperature
draw.text((590, 320), f"{pressure_in}", font=font, fill="black")    # Pressure
draw.text((950, 320), f"{vis_miles} mi", font=font, fill="black")   # Visibility
draw.text((1320, 320), f"{dew_f}°", font=font, fill="black")        # Dewpoint
draw.text((1700, 320), str(wind), font=font, fill="black")          # Winds

# ---- Save output ----
image.save(output_path)
