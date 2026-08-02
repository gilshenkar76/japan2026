from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/16.11.2026.png"
OUT = "assets/maps/day16_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((10, 1180, 400, 1400))  # 390 x 220
d = ImageDraw.Draw(card)


def font(sz):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def he(s):
    return s[::-1]


# Title bar
bg_title = card.getpixel((5, 5))
d.rectangle([0, 0, 390, 28], fill=bg_title)
d.text((195, 15), he("מפת מסלול היום"), font=font(15), fill=(60, 60, 150), anchor="mm")

# "Озеро Кавагути" -> "אגם קוואגוצ'י"
bgl = card.getpixel((237, 92))
d.rectangle([203, 93, 272, 118], fill=bgl)
d.text((237, 105), he("אגם קוואגוצ'י"), font=font(9), fill=(30, 30, 30), anchor="mm")

# Legend box: erase whole white box, redraw translated lines
bgleg = card.getpixel((16, 172))
d.rectangle([12, 170, 220, 216], fill=bgleg)
d.text((36, 180), he("בוקר: אתרי טבע"), font=font(10), fill=(40, 40, 40), anchor="lm")
d.text((36, 194), he("נסיעה באוטובוס"), font=font(10), fill=(40, 40, 40), anchor="lm")
d.text((36, 208), he("שינקנסן") + " Hikari", font=font(10), fill=(40, 40, 40), anchor="lm")

card.save(OUT)
print("saved", OUT, card.size)
