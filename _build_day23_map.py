"""Build day-23 route map: crop map card and translate Russian labels to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "updated_days/23_11_2026.jpeg"
OUT = "assets/maps/day23_route_map.png"

im = Image.open(SRC).convert("RGB")
# Map card in top-left of bottom section
card = im.crop((5, 1258, 265, 1376))   # 260 x 118
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


TITLE_BG = (255, 255, 255)
TITLE_FG = (30, 30, 100)
LEG_BG   = (255, 255, 255)
LEG_FG   = (60, 60, 60)

# --- Title bar: paint over Russian, write Hebrew ---
d.rectangle([0, 0, 260, 18], fill=TITLE_BG)
d.text((130, 9), he("מפת מסלול היום"), font=font(13), fill=TITLE_FG, anchor="mm")

# --- Legend: Пешком → רגלי, Транспорт → תחבורה ---
legend = [
    (100, "רגלי"),
    (111, "תחבורה"),
]
for y, txt in legend:
    d.rectangle([26, y - 6, 105, y + 7], fill=LEG_BG)
    d.text((28, y), he(txt), font=font(9), fill=LEG_FG, anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
