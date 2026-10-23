"""Crop attraction thumbnails from prep_days/27.11.2026.png into assets/attractions/day27/."""
import os
from PIL import Image

SRC = "prep_days/27.11.2026.png"
OUT = "assets/attractions/day27"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")
print(im.size)

# Calibrated photo-only boxes (title bar + QR/description excluded), 2 cols x 3 rows grid
boxes = [
    ("card1_sensoji",  300, 330, 645, 460),
    ("card2_nakamise", 655, 330, 1000, 460),
    ("card3_akihabara",300, 655, 645, 780),
    ("card4_skytree",  655, 655, 1000, 780),
    ("card5_solamachi",300, 970, 645, 1072),
    ("card6_dinner",   655, 970, 1000, 1072),
]
for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
cols, pad = 3, 6
thumb_w = max(c.width for c in crops)
max_h = max(c.height for c in crops)
rows = (len(crops) + cols - 1) // cols
sheet = Image.new("RGB", (cols*(thumb_w+pad)+pad, rows*(max_h+pad)+pad), (240,240,240))
for i, c in enumerate(crops):
    x = pad + (i % cols) * (thumb_w+pad)
    y = pad + (i // cols) * (max_h+pad)
    sheet.paste(c, (x, y))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"), quality=90)
