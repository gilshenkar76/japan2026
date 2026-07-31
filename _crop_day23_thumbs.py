"""Crop attraction thumbnails from updated_days/23_11_2026.jpeg into assets/attractions/day23/."""
import os
from PIL import Image

SRC = "updated_days/23_11_2026.jpeg"
OUT = "assets/attractions/day23"
os.makedirs(OUT, exist_ok=True)

im = Image.open(SRC).convert("RGB")

# Photos column x:458-697; row separators at y: 289,430,581,716,856,993,1142,1254
boxes = [
    ("sumiyoshi",   458, 293, 697, 426),
    ("kaiyukan",    458, 434, 697, 577),
    ("tempozan",    458, 585, 697, 712),
    ("abeno",       458, 720, 697, 852),
    ("shinsaibashi",458, 860, 697, 989),
    ("teamlab",     458, 997, 697, 1138),
    ("hotel",       458, 1146, 697, 1250),
]

for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)

crops = [im.crop((l, t, r, b)) for _, l, t, r, b in boxes]
cols, pad = 4, 6
thumb_w = crops[0].width
max_h = max(c.height for c in crops)
rows = (len(crops) + cols - 1) // cols
sheet = Image.new("RGB", (cols*(thumb_w+pad)+pad, rows*(max_h+pad)+pad), (240,240,240))
for i, c in enumerate(crops):
    sheet.paste(c, (pad+(i%cols)*(thumb_w+pad), pad+(i//cols)*(max_h+pad)))
sheet.save(os.path.join(OUT, "_contact_sheet.jpg"), quality=85)
print("done", len(boxes), "crops")
