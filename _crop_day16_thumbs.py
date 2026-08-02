"""Crop attraction thumbnails from prep_days/16.11.2026.png into assets/attractions/day16/."""
import os
from PIL import Image

SRC = "prep_days/16.11.2026.png"
OUT = "assets/attractions/day16"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")

boxes = [
    ("chureito",  468, 185, 742, 302),
    ("oshino",    468, 312, 742, 429),
    ("maple",     468, 439, 742, 556),
    ("lunch",     468, 566, 742, 683),
    ("transfer",  468, 693, 742, 810),
    ("checkin",   468, 820, 742, 937),
    ("evening",   468, 947, 742, 1064),
]
for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

w, h = 274, 117
sheet = Image.new("RGB", (w, h * len(boxes)), "white")
for i, (name, *_ ) in enumerate(boxes):
    thumb = Image.open(os.path.join(OUT, f"{name}.jpg"))
    sheet.paste(thumb, (0, i * h))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"))
print("done", len(boxes))
