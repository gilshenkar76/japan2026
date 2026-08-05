"""Build day-20 route map: crop full map card (title + map + legend) and translate Russian to Hebrew."""
from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/20.11.2026.png"
OUT = "assets/maps/day20_route_map.png"
SCALE = 2  # upscale for sharper output

im = Image.open(SRC).convert("RGB")
# Crop below the Russian title bar; we'll draw our own Hebrew title at top
card = im.crop((672, 128, 1024, 800))   # 352 × 672
W, H = card.size
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


PURPLE = (75, 20, 95)
WHITE  = (255, 255, 255)
DARK   = (30, 20, 20)
SOFT   = (60, 40, 30)

# --- Hebrew title bar replaces the Russian one ---
d.rectangle([0, 0, W, 30], fill=PURPLE)
d.text((W // 2, 15), he("מפת מסלול היום"), font=font(15), fill=WHITE, anchor="mm")

# --- Per-pin label redraw (coordinates from measured crop slices) ---
# Use WHITE fill so we always paint over source text regardless of its color
LABEL_BG = (255, 255, 255)
labels = [
    ( 68,  36, 185,  54, "Tōdai-ji",       "(מקדש טודאי-ג'י)"),
    (132, 150, 295, 100, "Nara Park",      "(פארק נארה)"),
    (190, 196, W-2, 175, "Kasuga Taisha",  "(קסוגה טאישה)"),
    (264, 130, W-2, 244, "Lunch",          "(ארוחת צהריים)"),
    (373,  88, W-2, 357, "Kofuku-ji",      "(מקדש קופוקו-ג'י)"),
    (440,  28, 235, 424, "Nara Machi",     "(העיר העתיקה)"),
]
for y0, x0, x1, y_top, name, he_txt in labels:
    d.rectangle([x0, y_top, x1, y0 + 32], fill=LABEL_BG)
    d.text((x0 + 4, y0),      name,       font=font(13), fill=DARK, anchor="lm")
    d.text((x0 + 4, y0 + 17), he(he_txt), font=font(11), fill=SOFT, anchor="lm")

# secondary Kasuga tent icon below the label box — keep ABOVE the Lunch label (y<244)
bg_ks2 = card.getpixel((10, 234))
d.rectangle([150, 224, W - 2, 243], fill=bg_ks2)

# small secondary fork+(Обед) map marker below the Lunch label
bg_fork = card.getpixel((10, 322))
d.rectangle([130, 298, W - 2, 352], fill=bg_fork)

# --- "7 Возвращение в Киото" (two-line label + on-route bus marker) ---
d.rectangle([28, 544, 170, 634], fill=LABEL_BG)
d.text((32, 566), he("חזרה לקיוטו"), font=font(13), fill=DARK, anchor="lm")

# --- Legend: "Пешком" → "רגלי", "Поезд JR Nara Line" → "JR Nara Line" ---
bg_leg = card.getpixel((10, 600))
d.rectangle([155, 589, W - 2, 612], fill=bg_leg)
d.text((195, 600), he("רגלי"), font=font(11), fill=DARK, anchor="lm")
d.rectangle([155, 607, W - 2, 652], fill=bg_leg)
d.text((195, 622), "JR Nara Line", font=font(11), fill=DARK, anchor="lm")

# --- Upscale 2× for quality ---
out_img = card.resize((W * SCALE, H * SCALE), Image.LANCZOS)
out_img.save(OUT)
print("saved", OUT, out_img.size)
