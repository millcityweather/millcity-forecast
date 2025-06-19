import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Load template
template = Image.open("weathercam_template.png").convert("RGBA")
draw = ImageDraw.Draw(template)

# Font setup
font_path = "helvetica-neue-lt-std-83-heavy-extended_CRtS6.otf"
font = ImageFont.truetype(font_path, 96)

# Get NWS data (Lowell, MA station)
points_url = "https://api.weather.gov/points/42.6334,-71.3162"
metadata = requests.get(points_url).json()
station_url = metadata["properties"]["observationStations"]

# Get the closest station's observations
stations = requests.get(station_url).json()
station_id = stations["features"][0]["properties"]["stationIdentifier"]
obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
obs = requests.get(obs_url).json()["properties"]

# Extract values
temperature = round(obs["temperature"]["value"] * 9 / 5 + 32) if obs["temperature"] else "--"
dewpoint = round(obs["dewpoint"]["value"] * 9 / 5 + 32) if obs["dewpoint"] else "--"
pressure = round(obs["barometricPressure"]["value"] * 0.0002953, 2) if obs["barometricPressure"] else "--"
visibility = round(obs["visibility"]["value"] / 1609.34) if obs["visibility"] else "--"
wind_dir = obs["windDirection"]["value"]
wind_speed = round(obs["windSpeed"]["value"] * 0.621371) if obs["windSpeed"] else "--"

# Convert wind direction to cardinal
def wind_direction(deg):
    if deg is None:
        return "--"
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    i = int((deg + 22.5) / 45) % 8
    return dirs[i]

wind_cardinal = wind_direction(wind_dir)

# Define positions
positions = {
    "temperature": (620, 80),
    "pressure": (620, 230),
    "visibility": (620, 380),
    "dewpoint": (620, 530),
    "winds": (620, 680)
}

# Draw text
draw.text(positions["temperature"], f"{temperature}°", font=font, fill="black")
draw.text(positions["pressure"], f"{pressure}", font=font, fill="black")
draw.text(positions["visibility"], f"{visibility} mi", font=font, fill="black")
draw.text(positions["dewpoint"], f"{dewpoint}", font=font, fill="black")
draw.text(positions["winds"], f"{wind_cardinal} {wind_speed}", font=font, fill="black")

# Save result
template.save("weathercam.png")

