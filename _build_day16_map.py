"""Build the day-16 Hakone/Fuji to Kyoto route map from OpenStreetMap tiles."""
import io
import math
import urllib.request

from PIL import Image, ImageDraw, ImageFont

OUT = "assets/maps/day16_route_map.png"
WIDTH, MAP_HEIGHT = 1200, 420
TITLE_HEIGHT, LEGEND_HEIGHT = 64, 70
BOUNDS = (135.50, 34.75, 139.30, 35.70)

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
card.paste(build_map(BOUNDS, 7, WIDTH), (0, TITLE_HEIGHT))
draw = ImageDraw.Draw(card)

navy = (30, 41, 79)
drive = (15, 118, 110)
rail = (49, 80, 190)
draw.rectangle((0, 0, WIDTH, TITLE_HEIGHT), fill=navy)
draw.text((WIDTH // 2, TITLE_HEIGHT // 2), he("מהאקונה דרך פוג'י לתחנת קיוטו"), font=font(28, True), fill="white", anchor="mm")

anchors = {key: point(key, BOUNDS, 7, WIDTH) for key in STOPS}
for points, color in (
    ([anchors[key] for key in ("hakone", "chureito", "oshino", "maple", "mishima")], drive),
    ([anchors["mishima"], anchors["kyoto"]], rail),
):
    draw.line(points, fill="white", width=13, joint="curve")
    draw.line(points, fill=color, width=8, joint="curve")


def marker(key, number, label, display_offset, label_offset, color=navy):
    anchor_x, anchor_y = anchors[key]
    x, y = anchor_x + display_offset[0], anchor_y + display_offset[1]
    if (x, y) != (anchor_x, anchor_y):
        draw.line((anchor_x, anchor_y, x, y), fill="white", width=7)
        draw.line((anchor_x, anchor_y, x, y), fill=color, width=3)
    draw.ellipse((x - 24, y - 24, x + 24, y + 24), fill="white", outline=color, width=5)
    draw.text((x, y), str(number), font=font(23, True), fill=color, anchor="mm")
    tx, ty = x + label_offset[0], y + label_offset[1]
    label_font = font(22, True)
    box = draw.textbbox((tx, ty), label, font=label_font, anchor="mm")
    draw.rounded_rectangle((box[0] - 8, box[1] - 5, box[2] + 8, box[3] + 5), radius=7, fill="white", outline=(175, 186, 204), width=2)
    draw.text((tx, ty), label, font=label_font, fill=(24, 31, 48), anchor="mm")


marker("hakone", 1, "Aura Tachibana", (-10, 20), (-60, -60))
marker("chureito", 2, "Chureito Pagoda", (-145, -5), (-105, -34))
marker("oshino", 3, "Oshino Hakkai", (-95, 70), (-100, 34))
marker("maple", 4, "Maple Corridor", (50, -20), (0, -38))
marker("mishima", 5, "Mishima Station", (-105, 50), (-105, 34), rail)
marker("kyoto", 6, "Kyoto Station", (20, 0), (100, -34), rail)

legend_y = TITLE_HEIGHT + MAP_HEIGHT
draw.rectangle((0, legend_y, WIDTH, legend_y + LEGEND_HEIGHT), fill=(248, 250, 252))
for x, color, label in ((100, drive, "מיניוואן פרטי"), (410, rail, "Hikari שינקנסן")):
    draw.line((x, legend_y + 29, x + 52, legend_y + 29), fill=color, width=8)
    draw.text((x + 66, legend_y + 29), he(label), font=font(22, True), fill=(35, 41, 54), anchor="lm")
draw.text((WIDTH - 12, legend_y + 58), "© OpenStreetMap contributors", font=font(12), fill=(90, 98, 112), anchor="rm")

card.save(OUT, optimize=True)
print("saved", OUT, card.size)
