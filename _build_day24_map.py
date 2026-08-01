"""Build day-24 route map: crop map card from source and translate Russian to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/24.11.2026.png"
OUT = "assets/maps/day24_route_map.png"

im = Image.open(SRC).convert("RGB")
# Map card: title + schematic Ginza/Shinjuku pin map (bottom-right of source image)
card = im.crop((768, 1199, 1022, 1445))   # 254 x 246
d = ImageDraw.Draw(card)


def font(sz):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def he(s):
    # Reverse pure-Hebrew string so PIL LTR draw renders RTL correctly
    return s[::-1]


TITLE_BG = (0, 24, 53)     # dark navy title bar background in this map style
TITLE_FG = (255, 255, 255)

# --- Title bar: paint over Russian "КАРТА МАРШРУТА ДНЯ", write Hebrew ---
d.rectangle([0, 2, 254, 31], fill=TITLE_BG)
d.text((127, 16), he("מפת מסלול היום"), font=font(14), fill=TITLE_FG, anchor="mm")

card.save(OUT)
print("saved", OUT, card.size)
