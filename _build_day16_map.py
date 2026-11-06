"""Build the day-16 Hakone/Fuji to Kyoto route map from OpenStreetMap tiles."""
import io
import math
import urllib.request

from PIL import Image, ImageDraw, ImageFont

OUT = "assets/maps/day16_route_map.png"
WIDTH, MAP_HEIGHT = 1000, 470
TITLE_HEIGHT, LEGEND_HEIGHT, GAP = 62, 70, 14
LEFT_WIDTH = 610
RIGHT_WIDTH = WIDTH - LEFT_WIDTH - GAP
LOCAL_BOUNDS = (138.70, 35.10, 139.14, 35.58)
REGIONAL_BOUNDS = (135.55, 34.84, 139.05, 35.48)

STOPS = {
    "hakone": (35.2273, 139.1042),
    "chureito": (35.5013, 138.8014),
    "oshino": (35.4601, 138.8327),
    "maple": (35.5229, 138.7645),
    "mishima": (35.1264, 138.9107),
    "kyoto": (34.9858, 135.7588),
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


def world_pixel(lat, lon, zoom):
    scale = 256 * (2**zoom)
    x = (lon + 180.0) / 360.0 * scale
    sin_lat = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale
    return x, y


def build_map(bounds, zoom, width):
    west, south, east, north = bounds
    left, top = world_pixel(north, west, zoom)
    right, bottom = world_pixel(south, east, zoom)
    x0, y0 = int(left // 256), int(top // 256)
    x1, y1 = int(right // 256), int(bottom // 256)
    mosaic = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    headers = {"User-Agent": "Japan2026TripMap/1.0"}
    for tile_x in range(x0, x1 + 1):
        for tile_y in range(y0, y1 + 1):
            request = urllib.request.Request(
                f"https://tile.openstreetmap.org/{zoom}/{tile_x}/{tile_y}.png", headers=headers
            )
            with urllib.request.urlopen(request) as response:
                tile = Image.open(io.BytesIO(response.read())).convert("RGB")
            mosaic.paste(tile, ((tile_x - x0) * 256, (tile_y - y0) * 256))
    crop = (
        round(left - x0 * 256), round(top - y0 * 256),
        round(right - x0 * 256), round(bottom - y0 * 256),
    )
    source = mosaic.crop(crop)
    scale = min(width / source.width, MAP_HEIGHT / source.height)
    rendered = source.resize(
        (round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS
    )
    panel = Image.new("RGB", (width, MAP_HEIGHT), (232, 238, 232))
    panel.paste(rendered, ((width - rendered.width) // 2, (MAP_HEIGHT - rendered.height) // 2))
    return panel


def point(key, bounds, zoom, width, x_offset=0):
    west, south, east, north = bounds
    lat, lon = STOPS[key]
    left, top = world_pixel(north, west, zoom)
    right, bottom = world_pixel(south, east, zoom)
    scale = min(width / (right - left), MAP_HEIGHT / (bottom - top))
    rendered_width = (right - left) * scale
    rendered_height = (bottom - top) * scale
    x_pad = (width - rendered_width) / 2
    y_pad = (MAP_HEIGHT - rendered_height) / 2
    world_x, world_y = world_pixel(lat, lon, zoom)
    return (
        round(x_offset + x_pad + (world_x - left) * scale),
        round(TITLE_HEIGHT + y_pad + (world_y - top) * scale),
    )


card = Image.new("RGB", (WIDTH, TITLE_HEIGHT + MAP_HEIGHT + LEGEND_HEIGHT), "white")
card.paste(build_map(LOCAL_BOUNDS, 10, LEFT_WIDTH), (0, TITLE_HEIGHT))
card.paste(build_map(REGIONAL_BOUNDS, 7, RIGHT_WIDTH), (LEFT_WIDTH + GAP, TITLE_HEIGHT))
draw = ImageDraw.Draw(card)

navy = (30, 41, 79)
drive = (15, 118, 110)
rail = (49, 80, 190)
draw.rectangle((0, 0, WIDTH, TITLE_HEIGHT), fill=navy)
draw.text((WIDTH // 2, TITLE_HEIGHT // 2), he("מהאקונה דרך פוג'י לתחנת קיוטו"), font=font(28, True), fill="white", anchor="mm")
draw.rectangle((LEFT_WIDTH, TITLE_HEIGHT, LEFT_WIDTH + GAP, TITLE_HEIGHT + MAP_HEIGHT), fill="white")

local_points = [point(key, LOCAL_BOUNDS, 10, LEFT_WIDTH) for key in ("hakone", "chureito", "oshino", "maple", "mishima")]
regional_points = [
    point("mishima", REGIONAL_BOUNDS, 7, RIGHT_WIDTH, LEFT_WIDTH + GAP),
    point("kyoto", REGIONAL_BOUNDS, 7, RIGHT_WIDTH, LEFT_WIDTH + GAP),
]
for points, color in ((local_points, drive), (regional_points, rail)):
    draw.line(points, fill="white", width=13, joint="curve")
    draw.line(points, fill=color, width=8, joint="curve")


def marker(position, number, label, offset, color=navy):
    x, y = position
    draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill="white", outline=color, width=5)
    draw.text((x, y), str(number), font=font(23, True), fill=color, anchor="mm")
    tx, ty = x + offset[0], y + offset[1]
    label_font = font(22, True)
    box = draw.textbbox((tx, ty), label, font=label_font, anchor="mm")
    draw.rounded_rectangle((box[0] - 8, box[1] - 5, box[2] + 8, box[3] + 5), radius=7, fill="white", outline=(175, 186, 204), width=2)
    draw.text((tx, ty), label, font=label_font, fill=(24, 31, 48), anchor="mm")


marker(local_points[0], 1, "Aura Tachibana", (-92, -35))
marker(local_points[1], 2, "Chureito Pagoda", (112, 0))
marker(local_points[2], 3, "Oshino Hakkai", (112, 36))
marker(local_points[3], 4, "Maple Corridor", (100, -28))
marker(local_points[4], 5, "Mishima Station", (-98, -36), rail)
marker(regional_points[0], 5, "Mishima", (-58, -35), rail)
marker(regional_points[1], 6, "Kyoto Station", (78, -36), rail)

legend_y = TITLE_HEIGHT + MAP_HEIGHT
draw.rectangle((0, legend_y, WIDTH, legend_y + LEGEND_HEIGHT), fill=(248, 250, 252))
for x, color, label in ((100, drive, "מיניוואן פרטי"), (410, rail, "Hikari שינקנסן")):
    draw.line((x, legend_y + 29, x + 52, legend_y + 29), fill=color, width=8)
    draw.text((x + 66, legend_y + 29), he(label), font=font(22, True), fill=(35, 41, 54), anchor="lm")
draw.text((WIDTH - 12, legend_y + 58), "© OpenStreetMap contributors", font=font(12), fill=(90, 98, 112), anchor="rm")

card.save(OUT, optimize=True)
print("saved", OUT, card.size)
