from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import dropbox

# === Dropbox Settings ===
DROPBOX_ACCESS_TOKEN = "sl.u.AFwlLGwmEmgHEV9ZWrxA8nF5ed1KctqtpMUH58qulSlF3VzTh9xAOFnN7oez3r5Hj3FnJkUjXfb_7XyOVFbsjeYERnuewabkp2vCF6mOqaC85Sj0ZDLLas9xyFRKPGNa5mH79cJ-aKztETZ9QWTYkf6icv0aai6YGR62Bq5u76AC4zVrYP7vddqX4xgOuafuS4WRWtg0urXRfLQduuPfMrSKp4MejCnzE_UPIUdW9M2yhfe8QH6a9nAghTyTwAhfY7svTAlhMiZr6LTF1dSqLIO3C_OS_QAg4p56viYNI_K94G-ZbEZ1aEf-7gkcv64wGHGnXpQ28RtfiTWBmoAIIK_cLtH85xNjEUviM3NTbq1ztQ-cJQEHI2JdcMIay2APc9B_GGHlf8ZKzUCBSabhgbYxDpIj_tX0Rhbv3y4YdzdDvv4iKB9BR3cwllDY26krWi6RnfUWgbRtitlS68Nk_G40jstL3V4h1uYmvfVskG1Lh1s0J86dmLfyg7r4gTxIDFJ2S0knYzmSg-4NBO-QEnAV0wz7BRCl2yyJLSZsgMPcR7lkqXgsAqqkTyajKTnWEEU8kUuO7v41s5BYqbv3T1CWUgls4pgyDwfFMHMKiLnLp2z7U7IFIsTY2znDkWSWQ6VQohe_BiYprricZRXLj67SFHPJLU6eQijk8jAoPG7Q-Dj5-fYm2vMxaRkEx2Yahe-pocHPinLQudE_-YPir8r1PkXUZoJYSKEjgEFS7N2_it-rswtcIGIofeXlqhKahPKs_4NHdZIW4wPfaAlhgYNuGG5GjIUV3YFbeQTr5_Ppehf9gHmJyXY-75XC3lXWeutLBrA9XERN0QtVUo7mnnfI1qvmDeakSFPzgmhoB61vKzJmeQMk83aVvpAn7Jhdf3qvfPJJ9nfltEBrqXSARNStQQay69E2uA_MYSg8Aw1HH-WaKvGzms0okgswdZrUMqU_9TQt7DGpHvRlKogcdUIo2arcMoZfMbFeCrPAgahajsBxHYNns1zqed43mYxo_8KnUDLkXvcmn60Noy-8ac_28tt9TPmt1JDU0xY0WwqDgrQGDv8GkwY0ok0r6iNVdKI0QDk5cQTtZygxKlVSioG5Cd58Ghl57Oy5qCI2oqfu-vApICTQdmKz0sK12oruhhi41ulLx0P6VKOHx0QYBgxvOHdU1Wtz-K29pu1iZrZwYo9YfugQuo4vkyTABSD7aQSiWhPY1GkVmgdKKtsE7misX5KBp5ywF9gmJxgS91w_7gyaKB9zmvRnDV1t2Q1xmesmOcEetvfIz_IPc5Ogisv8"
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


