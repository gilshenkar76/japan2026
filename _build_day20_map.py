"""Build day-20 route map: crop map card from source and translate Russian labels to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/20.11.2026.png"
OUT = "assets/maps/day20_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((690, 128, 1024, 745))   # 334 x 617 (legend box excluded)
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


# Title bar (solid purple)
d.rectangle([0, 0, 334, 24], fill=(75, 20, 95))
d.text((167, 12), he("מפת מסלול היום"), font=font(14), fill=(255, 255, 255), anchor="mm")

# Full two-line label redraw per pin (English name kept + fresh Hebrew translation)
labels = [
    (45,  "Tōdai-ji",      "(מקדש טודאי-ג'י)"),
    (120, "Nara Park",     "(פארק נארה)"),
    (196, "Kasuga Taisha", "(קסוגה טאישה)"),
    (308, "Lunch",         "(ארוחת צהריים)"),
    (375, "Kofuku-ji",     "(מקדש קופוקו-ג'י)"),
    (450, "Nara Machi",    "(העיר העתיקה)"),
]
for y0, name, he_txt in labels:
    bg = card.getpixel((5, y0 + 5))
    d.rectangle([30, y0 - 10, 334, y0 + 27], fill=bg)
    d.text((34, y0), name, font=font(13), fill=(30, 20, 20), anchor="lm")
    d.text((34, y0 + 17), he(he_txt), font=font(11), fill=(60, 40, 30), anchor="lm")

# extra cleanup for residual Russian sliver above Tōdai-ji label
d.rectangle([30, 70, 270, 90], fill=card.getpixel((5, 75)))
d.rectangle([290, 195, 334, 215], fill=card.getpixel((325, 230)))    # small in-map pin annotation
d.rectangle([280, 190, 334, 245], fill=card.getpixel((330, 255)))    # small in-map pin annotation (best-effort)

# "Возвращение в Киото" (bottom) -> single Hebrew line
bg2 = card.getpixel((5, 599))
d.rectangle([30, 582, 230, 618], fill=bg2)
d.text((34, 599), he("חזרה לקיוטו"), font=font(13), fill=(30, 20, 20), anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
