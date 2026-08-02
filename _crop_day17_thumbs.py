"""Crop attraction thumbnails from prep_days/17.11.2026.png into assets/attractions/day17/."""
import os
from PIL import Image

SRC = "prep_days/17.11.2026.png"
OUT = "assets/attractions/day17"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")

boxes = [
    ("toyota",     468, 187, 742, 302),
    ("shinkansen", 468, 332, 742, 447),
    ("hotel",      468, 477, 742, 592),
    ("teramachi",  468, 622, 742, 737),
    ("pontocho",   468, 767, 742, 882),
    ("return",     468, 912, 742, 1027),
]
for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

w, h = 274, 115
sheet = Image.new("RGB", (w, h * len(boxes)), "white")
for i, (name, *_ ) in enumerate(boxes):
    thumb = Image.open(os.path.join(OUT, f"{name}.jpg"))
    sheet.paste(thumb, (0, i * h))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"))
print("done", len(boxes))
