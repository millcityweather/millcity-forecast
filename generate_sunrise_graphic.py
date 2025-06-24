from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import pytz
import os
import dropbox

# === Dropbox Settings ===
DROPBOX_ACCESS_TOKEN = os.environ.get (sl.u.AFynP0GLkl2OY9obdIwEHHrdsUn4OaDcIgny8QGvctimec8VCkHfseCFfxpO3K4nioNjK87p17XuG16iS1dMuat9DcGsxdwamQ5r_SZAxukGfYWGt1mOe9aFKd6B1ldWvNFtIwnKCX0sBrLbbz2KYpQemr9p_v7SE1gn4NwikxmcGVRObt66rbD3ns4_flSWnSNlQ6fZQK9J3tnHKHIDo3ajg29jXOa0EBFQg5SX-nDYE0S5hNOPaLZqkfjD6dTkM2q9NlxQQid5dLOpm5ePX5ZbvaVRuAHiev4vo2JTE3wf1Y27EeqhQ5SCmEFVFGPfLrdhQbZdgkc0QMRCB2taazGZCJodRVC96oGNtb1eZijUvWk_rZYk5YwgCJJNPY2jDX-h1dsmdwg6th16W67NfhUCfshwUU8cZzh9_72pVsEB7HL-q5M0SWEdU6Y2OXXmb52XQujnJkKiHtVnmINex9Wcr0UzWCPHxi0xqflaiazgfxz9Yag9sgqi4Qi6ep03C6mwg5gu_OUpVKAy2H4wgqLM141brdatU9bRoX2TXfgGGn8aHuHSSKEE3ANFQiIuZybeVUvqJE32oZwVl_w0YR1jpRLbVk36ELCwmXHfhBOGPV0eBNNf1sbHZNfCniJiEp55GKd8dt8jyvSHCSNSK7i3ZdsKGSwGDwS_AUoAUL3iB9JUyNWlvM4Sfs_zLJj_IpCk-KeNip54AJvRePkcUGUkdYFt4-6GGZlMENqT1pYhufXviythw6scFX5yUn6uy-Z-1QMtCyZYPkQAOU8FUQ3P7VPAnFuh-zedCuuop3CBlJYkhL6dID92QxWdxqFiWzqR5wY6iGr4csQxIp093OpGFjSUA2k5C8GkBa9r7AMAH7qQgaV9U9x1JiFqHwCj66YeaypF0S2ELAytkco6llOHvpNkKYp3ewOYhX3YeewIJHKkpRm1hn7v5qBIuNjagVHgPvMIXPM8pIXP0zkr4lqqFRPxq0fg2YqB3FcsSXeW_jIcAGbkjVf9OD19XalkTSpMrPeECUJWjQhPx2_K09pcUfZiSx47W-rYt7Wg6czY5iIBJSpgHztPY59SrW0hISppYzJIeKVbetM1EZomZwY5SOvLr0avr5JUtl6Jx62uaO376-krM7GBP00yjaYecuQ5fghOseLi2Izmj_uyPufOILcDhbpf1qAG0SqDEbTPMVjVRnAmFVIhd1oA54Eb__liUURnlsRBMy5pjkGyCJGd7hlHa-Zyulgt26riY6PU0eo5HFMC9QDz_JpH7lIqEXduRX8tPXc-qG3OtnWYjFjo
DROPBOX_DEST_PATH = "/sunrise_graphic.png"

# === File Paths ===
TEMPLATE_PATH = "sunrisesunsettemplate.png"
OUTPUT_PATH = "sunrise_graphic.png"
FONT_PATH = "assets/fonts/Helvetica Neue LT Std 83 Heavy Extended.otf"

# === Load sunrise/sunset for Lowell, MA ===
def get_sunrise_sunset():
    url = "https://api.sunrise-sunset.org/json?lat=42.6334&lng=-71.3162&formatted=0"
    response = requests.get(url)
    data = response.json()["results"]
    sunrise_utc = datetime.fromisoformat(data["sunrise"])
    sunset_utc = datetime.fromisoformat(data["sunset"])
    eastern = pytz.timezone("US/Eastern")
    sunrise = sunrise_utc.astimezone(eastern).strftime("%-I:%M %p")
    sunset = sunset_utc.astimezone(eastern).strftime("%-I:%M %p")
    return sunrise, sunset

# === Upload to Dropbox ===
def upload_to_dropbox(local_path, dropbox_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
    print("✅ Uploaded to Dropbox:", dropbox_path)

# === Main Logic ===
def main():
    sunrise, sunset = get_sunrise_sunset()

    image = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 125)

    # Positions
    x = 710
    draw.text((x, 410), sunrise, font=font, fill="gold")
    draw.text((x, 660), sunset, font=font, fill="gold")

    image.save(OUTPUT_PATH)
    print("✅ Graphic saved:", OUTPUT_PATH)

    upload_to_dropbox(OUTPUT_PATH, DROPBOX_DEST_PATH)

if __name__ == "__main__":
    main()



