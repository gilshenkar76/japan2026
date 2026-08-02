from PIL import Image, ImageDraw, ImageFont

SRC = "prep_days/17.11.2026.png"
OUT = "assets/maps/day17_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((10, 1070, 512, 1370))  # 502 x 300
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
d.rectangle([0, 0, 502, 38], fill=bg_title)
d.text((251, 20), he("מפת מסלול הערב בקיוטו"), font=font(15), fill=(60, 60, 150), anchor="mm")

# "Река Камо" -> "נהר קאמו"
bgr = card.getpixel((478, 62))
d.rectangle([450, 60, 500, 90], fill=bgr)
d.text((478, 75), he("נהר קאמו"), font=font(10), fill=(60, 60, 60), anchor="mm")

# distance labels
bg1 = card.getpixel((195, 120))
d.rectangle([140, 113, 252, 154], fill=bg1)
d.text((197, 125), "≈ 10 " + he("דק'"), font=font(11), fill=(30, 30, 30), anchor="mm")
d.text((197, 143), "(900 " + he("מ'") + ")", font=font(11), fill=(30, 30, 30), anchor="mm")

bg2 = card.getpixel((360, 120))
d.rectangle([308, 113, 418, 154], fill=bg2)
d.text((362, 125), "≈ 5 " + he("דק'"), font=font(11), fill=(30, 30, 30), anchor="mm")
d.text((362, 143), "(350 " + he("מ'") + ")", font=font(11), fill=(30, 30, 30), anchor="mm")

# Legend
bgl = card.getpixel((16, 272))
d.rectangle([12, 262, 460, 292], fill=bgl)
d.text((72, 277), he("רגלי"), font=font(11), fill=(30, 30, 30), anchor="mm")
d.text((250, 277), he("מסלול הטיול"), font=font(11), fill=(30, 30, 30), anchor="mm")

card.save(OUT)
print("saved", OUT, card.size)
