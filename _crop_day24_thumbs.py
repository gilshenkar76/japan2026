"""Crop attraction thumbnails from prep_days/24.11.2026.png into assets/attractions/day24/.
First pass with rough boxes - refine after viewing the contact sheet.
"""
import os
from PIL import Image

SRC = "prep_days/24.11.2026.png"
OUT = "assets/attractions/day24"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")
print("source size", im.size)

boxes = [
    ("shinkansen", 363, 100, 690, 230),
    ("hotel_tokyo", 696, 100, 1021, 230),
    ("uobei", 366, 338, 690, 463),
    ("ginza_six", 699, 338, 1021, 463),
    ("nissan", 366, 675, 690, 785),
    ("omoide", 699, 675, 1021, 785),
    ("golden_gai", 366, 980, 690, 1073),
    ("kabukicho", 699, 980, 1021, 1073),
]

for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

# contact sheet
cols = 4
thumb_w = 200
pad = 6
rows = (len(boxes) + cols - 1) // cols
crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
max_h = max(c.height for c in crops)
sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (max_h + pad) + pad), (240, 240, 240))
for i, c in enumerate(crops):
    rx = i % cols
    ry = i // cols
    c2 = c.resize((thumb_w, int(c.height * thumb_w / c.width)))
    sheet.paste(c2, (pad + rx * (thumb_w + pad), pad + ry * (max_h + pad)))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"), quality=85)
print("done", len(boxes), "crops")
