"""Build day-18 route map: crop map card from source and translate Russian title to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/18.11.2026.png"
OUT = "assets/maps/day18_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((5, 1310, 345, 1440))   # 340 x 130
d = ImageDraw.Draw(card)


def font(sz):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def he(s):
    return s[::-1]


BG = (243, 243, 252)
FG = (0, 0, 153)

d.rectangle([0, 0, 340, 19], fill=BG)
d.text((170, 10), he("מפת מסלול היום"), font=font(14), fill=FG, anchor="mm")

card.save(OUT)
print("saved", OUT, card.size)
