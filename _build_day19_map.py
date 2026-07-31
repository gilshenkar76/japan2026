"""Build day-19 route map: crop full original map (title + legend) and translate the
Russian title/legend to Hebrew (RTL), keeping English place labels and (Гион) as-is."""
from PIL import Image, ImageDraw, ImageFont

SRC = "updated_days/19_11_2026.jpeg"
OUT = "assets/maps/day19_route_map.png"

im = Image.open(SRC).convert("RGB")
# full map card: title bar + map + legend
card = im.crop((648, 116, 1016, 760))  # 368 x 644
d = ImageDraw.Draw(card)


def font(sz):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def he(s):
    # PIL draws LTR; reverse pure-Hebrew logical string for correct RTL display
    return s[::-1]


PURPLE = (48, 4, 93)
LEG_BG = (250, 246, 247)
LEG_TX = (60, 48, 130)

# --- title bar: paint over Russian, write Hebrew centered ---
d.rectangle([52, 4, 316, 33], fill=PURPLE)
d.text((184, 19), he("מפת מסלול היום"), font=font(20), fill=(255, 255, 255), anchor="mm")

# --- legend: paint over the three Russian words, write Hebrew (symbols kept) ---
legend = [
    (561, "רגלי"),
    (584, "תחבורה ציבורית"),
    (608, "מסלול ערב"),
]
for y, txt in legend:
    d.rectangle([203, y - 11, 346, y + 11], fill=LEG_BG)
    d.text((207, y), he(txt), font=font(13), fill=LEG_TX, anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
