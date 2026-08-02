"""Crop attraction thumbnails from prep_days/15.11.2026.png into assets/attractions/day15/."""
import os
from PIL import Image

SRC = "prep_days/15.11.2026.png"
OUT = "assets/attractions/day15"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")

boxes = [
    ("lake_ashi",  468, 185, 742, 302),
    ("pirate_ship",468, 312, 742, 429),
    ("ropeway",    468, 439, 742, 556),
    ("owakudani",  468, 566, 742, 683),
    ("lunch",      468, 693, 742, 810),
    ("museum",     468, 820, 742, 937),
    ("hotel",      468, 947, 742, 1064),
]
for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

# contact sheet for QA
w, h = 274, 117
sheet = Image.new("RGB", (w, h * len(boxes)), "white")
for i, (name, *_ ) in enumerate(boxes):
    thumb = Image.open(os.path.join(OUT, f"{name}.jpg"))
    sheet.paste(thumb, (0, i * h))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"))
print("done", len(boxes))
