"""Build day-15 route map: crop map card from source and translate Russian labels to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/15.11.2026.png"
OUT = "assets/maps/day15_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((10, 1150, 410, 1400))  # 400 x 250
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


# Title bar
bg_title = card.getpixel((5, 8))
d.rectangle([0, 30, 400, 55], fill=bg_title)
d.text((200, 42), he("מפת מסלול היום"), font=font(15), fill=(60, 60, 150), anchor="mm")

# Pin labels: erase only the Russian line, keep English lines as-is
bg1 = card.getpixel((65, 51))
d.rectangle([26, 44, 104, 73], fill=bg1)
d.text((65, 60), he("אגם אשי"), font=font(10), fill=(30, 30, 30), anchor="mm")

bg2 = card.getpixel((128, 80))
d.rectangle([88, 80, 168, 124], fill=bg2)
d.text((128, 98), he("ספינת פיראטים"), font=font(9), fill=(30, 30, 30), anchor="mm")

bg3 = card.getpixel((225, 86))
d.rectangle([186, 86, 266, 106], fill=bg3)
d.text((226, 96), he("אווקודאני"), font=font(10), fill=(30, 30, 30), anchor="mm")

bg4 = card.getpixel((262, 136))
d.rectangle([220, 136, 316, 156], fill=bg4)
d.text((268, 146), he("מוזיאון פתוח"), font=font(9), fill=(30, 30, 30), anchor="mm")

bgh = card.getpixel((305, 176))
d.rectangle([270, 174, 342, 192], fill=bgh)
d.text((306, 183), he("(מלון)"), font=font(10), fill=(30, 30, 30), anchor="mm")

# Legend: erase the whole white legend box once, redraw all 4 lines cleanly
bgl = card.getpixel((16, 198))
d.rectangle([14, 196, 176, 251], fill=bgl)
legend = [
    (206, "רגלי"),
    (219, "ספינה"),
    (232, "רכבל"),
    (245, "אוטובוס / העברה"),
]
for y, txt in legend:
    d.text((40, y), he(txt), font=font(10), fill=(40, 40, 40), anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
