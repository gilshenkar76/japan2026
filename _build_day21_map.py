"""Build day-21 route map: crop map card from source and translate Russian to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "updated_days/21_11_2026.jpeg"
OUT = "assets/maps/day21_route_map.png"

im = Image.open(SRC).convert("RGB")
# Map card: title + route + legend (bottom-left of source image)
card = im.crop((8, 1348, 380, 1470))   # 372 x 122
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


TITLE_BG = (255, 255, 255)   # white title bar background in this map style
TITLE_FG = (30, 30, 100)     # dark navy text
LEG_BG   = (255, 255, 255)
LEG_FX   = (60, 60, 60)

# --- Title bar: paint over Russian, write Hebrew ---
d.rectangle([0, 0, 372, 18], fill=TITLE_BG)
d.text((186, 9), he("מפת מסלול היום"), font=font(13), fill=TITLE_FG, anchor="mm")

# --- Node label patches: translate Russian words inside parentheses ---
# "(отель)" at node "Kyoto" → "(מלון)" — approx position in card
d.rectangle([6, 40, 62, 56], fill=(245, 243, 250))
d.text((8, 48), he("(מלון)"), font=font(9), fill=(80, 60, 140), anchor="lm")

# "(ужин)" at Wagyu node → "(ארוחת ערב)"
d.rectangle([292, 58, 360, 72], fill=(245, 243, 250))
d.text((294, 65), he("(ארוחת ערב)"), font=font(8), fill=(80, 60, 140), anchor="lm")

# --- Legend: translate three Russian labels ---
# Поезда → רכבת,  Пешком → רגלי,  Переезды → נסיעה
legend = [
    (93,  "רכבת"),
    (104, "רגלי"),
    (114, "נסיעה"),
]
for y, txt in legend:
    d.rectangle([26, y - 6, 100, y + 7], fill=LEG_BG)
    d.text((28, y), he(txt), font=font(9), fill=LEG_FX, anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
