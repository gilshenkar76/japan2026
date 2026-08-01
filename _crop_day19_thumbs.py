"""Crop attraction thumbnails from updated_days/19_11_2026.jpeg into assets/attractions/day19/."""
import os
from PIL import Image

SRC = "updated_days/19_11_2026.jpeg"
OUT = "assets/attractions/day19"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")

# (name, left, top, right, bottom) - precisely aligned to source photo bounds (no white-gap bleed)
boxes = [
    ("eikando",    103, 129, 293, 244),
    ("kiyomizu",   103, 262, 293, 375),
    ("sannenzaka", 103, 393, 293, 505),
    ("yasaka",     103, 523, 293, 634),
    ("lunch",      103, 651, 293, 756),
    ("shijo",      103, 770, 293, 877),
    ("hotel",      103, 894, 293, 981),
    ("kiyamachi",  103, 1019, 293, 1105),
    ("escamoteur", 103, 1117, 293, 1193),
    ("dinner",     103, 1203, 293, 1271),
    ("turquoise",  103, 1281, 293, 1334),
]

for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

# contact sheet for verification
cols = 4
thumb_w = 190
pad = 6
rows = (len(boxes) + cols - 1) // cols
# use max height
crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
max_h = max(c.height for c in crops)
sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (max_h + pad) + pad), (240, 240, 240))
for i, c in enumerate(crops):
    rx = i % cols
    ry = i // cols
    sheet.paste(c, (pad + rx * (thumb_w + pad), pad + ry * (max_h + pad)))
sheet.save("assets/attractions/day19/_contact_sheet.jpg", quality=85)
print("done", len(boxes), "crops")
