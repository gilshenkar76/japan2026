"""Crop attraction thumbnails from prep_days/20.11.2026.png into assets/attractions/day20/."""
import os
from PIL import Image

SRC = "prep_days/20.11.2026.png"
OUT = "assets/attractions/day20"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")
print("size", im.size)

boxes = [
    ("todaiji",   120, 130, 318, 260),
    ("narapark",  120, 260, 318, 390),
    ("kasuga",    120, 390, 318, 520),
    ("lunch",     120, 520, 318, 650),
    ("kofukuji",  120, 650, 318, 780),
    ("naramachi", 120, 780, 318, 910),
    ("train",     120, 910, 318, 1040),
]

for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

cols = 4
thumb_w = 180
pad = 6
rows = (len(boxes) + cols - 1) // cols
crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
max_h = max(c.height for c in crops)
sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (max_h + pad) + pad), (240, 240, 240))
for i, c in enumerate(crops):
    rx, ry = i % cols, i // cols
    c2 = c.resize((thumb_w, int(c.height * thumb_w / c.width)))
    sheet.paste(c2, (pad + rx * (thumb_w + pad), pad + ry * (max_h + pad)))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"), quality=85)
print("done")
