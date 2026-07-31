"""Crop attraction thumbnails from updated_days/19_11_2026.jpeg into assets/attractions/day19/."""
import os
from PIL import Image

SRC = "updated_days/19_11_2026.jpeg"
OUT = "assets/attractions/day19"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")

# (name, left, top, right, bottom)
boxes = [
    ("eikando",    103, 138, 293, 236),
    ("kiyomizu",   103, 258, 293, 356),
    ("sannenzaka", 103, 377, 293, 475),
    ("yasaka",     103, 495, 293, 605),
    ("lunch",      103, 613, 293, 713),
    ("shijo",      103, 770, 293, 878),
    ("hotel",      103, 905, 293, 985),
    ("kiyamachi",  103, 1030, 293, 1108),
    ("escamoteur", 103, 1112, 293, 1190),
    ("dinner",     103, 1200, 293, 1277),
    ("turquoise",  103, 1288, 293, 1356),
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
