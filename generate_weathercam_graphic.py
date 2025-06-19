import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# === Load base template ===
template = Image.open("weathercam_template.png").convert("RGBA")
draw = ImageDraw.Draw(template)

# === Load font ===
font_path = "helvetica-neue-lt-std-83-heavy-extended.otf"
font = ImageFont.truetype(font_path, 96)

# === Get NWS station data from Lowell, MA (01854) ===
points_url = "https://api.weather.gov/points/42.6334,-71.3162"
metadata = requests.get(points_url).json()
station_url = metadata["properties"]["observationStations"]

# === Get latest observation from nearest station ===
stations = requests.get(station_url).json()
station_id = stations["features"][0]["properties"]["stationIdentifier"]
obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
obs = requests.get(obs_url).json()["properties"]

# === Extract weather data with safety fallbacks ===
def safe_get(data, path, fallback="--"):
    for key in path:
        data = data.get(key, {})
    return data if isinstance(data, (int, float, str)) and data else fallback

temperature = round((obs.get("temperature", {}).get("value", 0) * 9 / 5) + 32) if obs.get("temperature") else "--"
dewpoint = round((obs.get("dewpoint", {}).get("value", 0) * 9 / 5) + 32) if obs.get("dewpoint") else "--"
pressure = round(obs.get("barometricPressure", {}).get("value", 0) * 0.0002953, 2) if obs.get("barometricPressure") else "--"
visibility = round(obs.get("visibility", {}).get("value", 0)

