import os
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Load environment variable for Dropbox
DROPBOX_ACCESS_TOKEN = os.environ.get("sl.u.AFynP0GLkl2OY9obdIwEHHrdsUn4OaDcIgny8QGvctimec8VCkHfseCFfxpO3K4nioNjK87p17XuG16iS1dMuat9DcGsxdwamQ5r_SZAxukGfYWGt1mOe9aFKd6B1ldWvNFtIwnKCX0sBrLbbz2KYpQemr9p_v7SE1gn4NwikxmcGVRObt66rbD3ns4_flSWnSNlQ6fZQK9J3tnHKHIDo3ajg29jXOa0EBFQg5SX-nDYE0S5hNOPaLZqkfjD6dTkM2q9NlxQQid5dLOpm5ePX5ZbvaVRuAHiev4vo2JTE3wf1Y27EeqhQ5SCmEFVFGPfLrdhQbZdgkc0QMRCB2taazGZCJodRVC96oGNtb1eZijUvWk_rZYk5YwgCJJNPY2jDX-h1dsmdwg6th16W67NfhUCfshwUU8cZzh9_72pVsEB7HL-q5M0SWEdU6Y2OXXmb52XQujnJkKiHtVnmINex9Wcr0UzWCPHxi0xqflaiazgfxz9Yag9sgqi4Qi6ep03C6mwg5gu_OUpVKAy2H4wgqLM141brdatU9bRoX2TXfgGGn8aHuHSSKEE3ANFQiIuZybeVUvqJE32oZwVl_w0YR1jpRLbVk36ELCwmXHfhBOGPV0eBNNf1sbHZNfCniJiEp55GKd8dt8jyvSHCSNSK7i3ZdsKGSwGDwS_AUoAUL3iB9JUyNWlvM4Sfs_zLJj_IpCk-KeNip54AJvRePkcUGUkdYFt4-6GGZlMENqT1pYhufXviythw6scFX5yUn6uy-Z-1QMtCyZYPkQAOU8FUQ3P7VPAnFuh-zedCuuop3CBlJYkhL6dID92QxWdxqFiWzqR5wY6iGr4csQxIp093OpGFjSUA2k5C8GkBa9r7AMAH7qQgaV9U9x1JiFqHwCj66YeaypF0S2ELAytkco6llOHvpNkKYp3ewOYhX3YeewIJHKkpRm1hn7v5qBIuNjagVHgPvMIXPM8pIXP0zkr4lqqFRPxq0fg2YqB3FcsSXeW_jIcAGbkjVf9OD19XalkTSpMrPeECUJWjQhPx2_K09pcUfZiSx47W-rYt7Wg6czY5iIBJSpgHztPY59SrW0hISppYzJIeKVbetM1EZomZwY5SOvLr0avr5JUtl6Jx62uaO376-krM7GBP00yjaYecuQ5fghOseLi2Izmj_uyPufOILcDhbpf1qAG0SqDEbTPMVjVRnAmFVIhd1oA54Eb__liUURnlsRBMy5pjkGyCJGd7hlHa-Zyulgt26riY6PU0eo5HFMC9QDz_JpH7lIqEXduRX8tPXc-qG3OtnWYjFjo")

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



