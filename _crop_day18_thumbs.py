"""Crop attraction thumbnails from prep_days/18.11.2026.png into assets/attractions/day18/."""
import os
from PIL import Image

SRC = "prep_days/18.11.2026.png"
OUT = "assets/attractions/day18"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")

boxes = [
    ("fushimi",   358, 348, 565, 460),
    ("bamboo",    358, 465, 565, 590),
    ("tenryuji",  358, 595, 565, 703),
    ("lunch",     358, 720, 565, 845),
    ("ryoanji",   358, 855, 565, 975),
    ("kinkakuji", 358, 980, 565, 1090),
    ("gion",      358, 1110, 565, 1235),
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
