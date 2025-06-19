# Function to center text inside a rectangle
def draw_centered_text(text, box_x, box_y, box_width, box_height, font):
    text_width, text_height = draw.textsize(text, font=font)
    x = box_x + (box_width - text_width) // 2
    y = box_y + (box_height - text_height) // 2
    draw.text((x, y), text, font=font, fill="black")

# White box coordinates (x, y, width, height)
boxes = [
    (845, 95, 450, 110),   # Temperature
    (845, 250, 450, 110),  # Pressure
    (845, 405, 450, 110),  # Visibility
    (845, 560, 450, 110),  # Dewpoint
    (845, 715, 450, 110),  # Winds
]

# Text values
values = [
    f"{temperature}°",
    f"{pressure}",
    f"{visibility} mi",
    f"{dewpoint}",
    f"{wind_text}"
]

# Draw them
for (x, y, w, h), text in zip(boxes, values):
    draw_centered_text(text, x, y, w, h, font)