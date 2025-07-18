import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from draw_centered_patch import draw_centered

# Load the template
template = Image.open("weathercam_template.png").convert("RGBA")
draw = ImageDraw.Draw(template)

# Font setup
font_path = "helvetica_neue_lt_std_83.otf"
font = ImageFont.truetype(font_path, 88)

# Get NWS data for Lowell, MA
points_url = "https://api.weather.gov/points/42.6334,-71.3162"
metadata = requests.get(points_url).json()
station_url = metadata["properties"]["observationStations"]

# Get latest observation
stations = requests.get(station_url).json()
station_id = stations["features"][0]["properties"]["stationIdentifier"]
obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
obs = requests.get(obs_url).json()["properties"]

# Extract values with fallback
def safe_get(key):
    return obs.get(key, {}).get("value")

temperature = round(safe_get("temperature") * 9 / 5 + 32) if safe_get("temperature") is not None else "--"
dewpoint = round(safe_get("dewpoint") * 9 / 5 + 32) if safe_get("dewpoint") is not None else "--"
pressure = round(safe_get("barometricPressure") * 0.0002953, 2) if safe_get("barometricPressure") is not None else "--"
visibility = round(safe_get("visibility") / 1609.34) if safe_get("visibility") is not None else "--"
wind_speed = round(safe_get("windSpeed") * 0.621371) if safe_get("windSpeed") is not None else "--"
wind_dir = safe_get("windDirection")

# Convert wind direction to cardinal
def deg_to_cardinal(deg):
    if deg is None:
        return "--"
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    return dirs[int((deg % 360) / 45) % 8]

wind_cardinal = deg_to_cardinal(wind_dir)
wind_text = f"{wind_cardinal} {wind_speed}"

# Draw centered text inside white boxes (x, y, width, height)
draw_centered(draw, f"{temperature}°", font, box=(830, 95, 400, 120))
draw_centered(draw, f"{pressure}", font, box=(830, 250, 400, 120))
draw_centered(draw, f"{visibility} mi", font, box=(830, 405, 400, 120))
draw_centered(draw, f"{dewpoint}", font, box=(830, 560, 400, 120))
draw_centered(draw, f"{wind_text}", font, box=(830, 715, 400, 120))

# Save the output
template.save("weathercam.png")

