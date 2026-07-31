"""Crop attraction thumbnails from updated_days/21_11_2026.jpeg into assets/attractions/day21/."""
import os
from PIL import Image

SRC = "updated_days/21_11_2026.jpeg"
OUT = "assets/attractions/day21"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")

# Photos are in center column x:458-697; rows detected from separator scan
# (name, left, top, right, bottom)
boxes = [
    ("nishiki",     458, 190, 697, 310),
    ("transfer",    458, 318, 697, 427),
    ("arrival",     458, 435, 697, 533),
    ("umeda_sky",   458, 541, 697, 650),
    ("grand_green", 458, 658, 697, 758),
    ("tullys",      458, 766, 697, 853),
    ("namba_city",  458, 861, 697, 950),
    ("namba_parks", 458, 958, 697, 1057),
    ("hotel",       458, 1065, 697, 1155),
    ("wagyu",       458, 1163, 697, 1241),
    ("nayuta",      458, 1249, 697, 1343),
]

for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

# contact sheet for verification
cols = 4
pad = 6
crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
thumb_w = crops[0].width
max_h = max(c.height for c in crops)
rows = (len(crops) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (max_h + pad) + pad), (240, 240, 240))
for i, c in enumerate(crops):
    sheet.paste(c, (pad + (i % cols) * (thumb_w + pad), pad + (i // cols) * (max_h + pad)))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"), quality=85)
print("done", len(boxes), "crops")
