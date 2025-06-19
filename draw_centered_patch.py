from PIL import ImageDraw

def draw_centered(draw: ImageDraw.Draw, text: str, font, box: tuple, fill="black"):
    """
    Draws text centered in the given box.
    box = (x, y, width, height)
    """
    x, y, w, h = box
    text_w, text_h = draw.textsize(text, font=font)
    text_x = x + (w - text_w) / 2
    text_y = y + (h - text_h) / 2
    draw.text((text_x, text_y), text, font=font, fill=fill)
