"""Build the full day-17 Kyoto route map from OpenStreetMap tiles."""
import io
import math
import urllib.request

from PIL import Image, ImageDraw, ImageFont

OUT = "assets/maps/day17_route_map.png"
WIDTH, MAP_HEIGHT = 900, 410
TITLE_HEIGHT, LEGEND_HEIGHT = 58, 72
ZOOM = 15
BOUNDS = (135.7415, 34.9995, 135.7985, 35.0190)  # west, south, east, north

STOPS = {
    "hotel": (35.0077882, 135.7592684),
    "nijo": (35.0140076, 135.7485369),
    "nishiki": (35.0050244, 135.7655699),
    "shiyakusho": (35.0108986, 135.7688702),
    "keage": (35.00735, 135.79075),
    "nanzenji": (35.0115254, 135.7927213),
    "miyabi": (35.0059460, 135.7700610),
}


def font(size, bold=False):
    names = ("arialbd.ttf", "arial.ttf") if bold else ("arial.ttf", "arialbd.ttf")
    for name in names:
        try:
            return ImageFont.truetype(rf"C:\Windows\Fonts\{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def he(text):
    return text[::-1]


def world_pixel(lat, lon):
    scale = 256 * (2**ZOOM)
    x = (lon + 180.0) / 360.0 * scale
    sin_lat = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale
    return x, y


def build_base_map():
    west, south, east, north = BOUNDS
    left, top = world_pixel(north, west)
    right, bottom = world_pixel(south, east)
    x0, y0 = int(left // 256), int(top // 256)
    x1, y1 = int(right // 256), int(bottom // 256)
    mosaic = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    headers = {"User-Agent": "Japan2026TripMap/1.0"}
    for tile_x in range(x0, x1 + 1):
        for tile_y in range(y0, y1 + 1):
            url = f"https://tile.openstreetmap.org/{ZOOM}/{tile_x}/{tile_y}.png"
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                tile = Image.open(io.BytesIO(response.read())).convert("RGB")
            mosaic.paste(tile, ((tile_x - x0) * 256, (tile_y - y0) * 256))
    crop = (
        round(left - x0 * 256),
        round(top - y0 * 256),
        round(right - x0 * 256),
        round(bottom - y0 * 256),
    )
    return mosaic.crop(crop).resize((WIDTH, MAP_HEIGHT), Image.Resampling.LANCZOS)


def point(key):
    west, south, east, north = BOUNDS
    lat, lon = STOPS[key]
    x = (lon - west) / (east - west) * WIDTH
    top_y = world_pixel(north, west)[1]
    bottom_y = world_pixel(south, west)[1]
    y = (world_pixel(lat, lon)[1] - top_y) / (bottom_y - top_y) * MAP_HEIGHT
    return round(x), round(y + TITLE_HEIGHT)


card = Image.new("RGB", (WIDTH, TITLE_HEIGHT + MAP_HEIGHT + LEGEND_HEIGHT), "white")
card.paste(build_base_map(), (0, TITLE_HEIGHT))
draw = ImageDraw.Draw(card)

draw.rectangle((0, 0, WIDTH, TITLE_HEIGHT), fill=(30, 41, 79))
draw.text((WIDTH // 2, TITLE_HEIGHT // 2), he("מפת מסלול היום בקיוטו"), font=font(25, True), fill="white", anchor="mm")

walk_color = (101, 48, 163)
metro_color = (22, 111, 181)
evening_color = (222, 91, 39)

draw.line([point("hotel"), point("nijo"), point("nishiki")], fill="white", width=12, joint="curve")
draw.line([point("hotel"), point("nijo"), point("nishiki")], fill=walk_color, width=7, joint="curve")
draw.line([point("nishiki"), point("shiyakusho"), point("keage"), point("nanzenji")], fill="white", width=12, joint="curve")
draw.line([point("nishiki"), point("shiyakusho"), point("keage"), point("nanzenji")], fill=metro_color, width=7, joint="curve")
draw.line([point("nanzenji"), point("keage"), point("shiyakusho"), point("miyabi")], fill="white", width=12, joint="curve")
draw.line([point("nanzenji"), point("keage"), point("shiyakusho"), point("miyabi")], fill=evening_color, width=7, joint="curve")


def marker(key, number, label, offset):
    x, y = point(key)
    color = (30, 41, 79)
    draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill="white", outline=color, width=4)
    draw.text((x, y), str(number), font=font(15, True), fill=color, anchor="mm")
    tx, ty = x + offset[0], y + offset[1]
    text_font = font(17, True)
    box = draw.textbbox((tx, ty), label, font=text_font, anchor="mm")
    draw.rounded_rectangle((box[0] - 8, box[1] - 5, box[2] + 8, box[3] + 5), radius=7, fill=(255, 255, 255, 235), outline=(210, 216, 226), width=2)
    draw.text((tx, ty), label, font=text_font, fill=(24, 31, 48), anchor="mm")


marker("hotel", 1, "Hotel Monterey", (15, 35))
marker("nijo", 2, "Nijo Castle", (55, -34))
marker("nishiki", 3, "Nishiki Market", (-48, 35))
marker("nanzenji", 4, "Nanzen-ji", (-62, -34))
marker("miyabi", 5, "MIYABI Drum Show", (82, 34))

for key, label, offset in (
    ("shiyakusho", "Kyoto Shiyakusho-mae", (88, -25)),
    ("keage", "Keage", (-35, 26)),
):
    x, y = point(key)
    draw.rectangle((x - 7, y - 7, x + 7, y + 7), fill=metro_color, outline="white", width=2)
    draw.text((x + offset[0], y + offset[1]), label, font=font(13, True), fill=(20, 67, 110), anchor="mm", stroke_width=3, stroke_fill="white")

legend_y = TITLE_HEIGHT + MAP_HEIGHT
draw.rectangle((0, legend_y, WIDTH, legend_y + LEGEND_HEIGHT), fill=(248, 250, 252))
items = ((walk_color, "רגלי"), (metro_color, "קו Tozai"), (evening_color, "חזרה למרכז ומופע"))
for index, (color, label) in enumerate(items):
    x = 120 + index * 260
    draw.line((x, legend_y + 29, x + 42, legend_y + 29), fill=color, width=7)
    draw.text((x + 55, legend_y + 29), he(label) if label != "קו Tozai" else "Tozai " + he("קו"), font=font(16, True), fill=(35, 41, 54), anchor="lm")
draw.text((WIDTH - 10, legend_y + 59), "© OpenStreetMap contributors", font=font(11), fill=(90, 98, 112), anchor="rm")

card.save(OUT, optimize=True)
print("saved", OUT, card.size)
