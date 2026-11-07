"""Build consistent, phone-readable route maps for all trip days except 16 and 17."""
import io
import math
import os
import sys
import tempfile
import urllib.request

from PIL import Image, ImageDraw, ImageFont

WIDTH = 900
TITLE_HEIGHT = 60
MAP_HEIGHT = 430
LEGEND_HEIGHT = 110
TOTAL_HEIGHT = TITLE_HEIGHT + MAP_HEIGHT + LEGEND_HEIGHT
TILE_CACHE = os.path.join(tempfile.gettempdir(), "japan2026_osm_tiles")

MODE_STYLES = {
    "walk": ((101, 48, 163), "רגלי"),
    "metro": ((22, 111, 181), "מטרו"),
    "train": ((17, 138, 82), "רכבת"),
    "shinkansen": ((190, 43, 59), "שינקנסן"),
    "bus": ((220, 92, 40), "אוטובוס / שאטל"),
    "taxi": ((203, 140, 22), "מונית / רכב"),
    "ship": ((8, 145, 178), "שייט"),
    "ropeway": ((205, 91, 145), "רכבל"),
    "flight": ((118, 45, 154), "טיסה"),
}


def stop(key, label, lat=None, lon=None):
    return {"key": key, "label": label, "lat": lat, "lon": lon}


def leg(start, end, mode):
    return (start, end, mode)


DAY_MAPS = {
    "12-13": {
        "layout": "geo",
        "title": "מפת מסלול הטיסה ליפן",
        "stops": [
            stop("tlv", "Ben Gurion Airport", 32.0055, 34.8854),
            stop("auh", "Abu Dhabi Airport", 24.4330, 54.6511),
            stop("nrt", "Narita Airport", 35.7720, 140.3929),
            stop("hotel", "Hotel Gracery Shinjuku", 35.6951, 139.7020),
        ],
        "legs": [leg("tlv", "auh", "flight"), leg("auh", "nrt", "flight"), leg("nrt", "hotel", "train")],
    },
    "14": {
        "layout": "geo",
        "title": "מפת מסלול טוקיו והאקונה",
        "stops": [
            stop("hotel", "Hotel Gracery", 35.6951, 139.7020),
            stop("tmg", "Tokyo Gov. Building", 35.6896, 139.6917),
            stop("gyoen", "Shinjuku Gyoen", 35.6852, 139.7101),
            stop("station", "Shinjuku Station", 35.6909, 139.7003),
            stop("hakone", "Hakone-Yumoto", 35.2334, 139.1037),
            stop("ryokan", "Aura Tachibana", 35.2289, 139.1028),
        ],
        "legs": [leg("hotel", "tmg", "walk"), leg("tmg", "gyoen", "walk"),
                 leg("gyoen", "station", "walk"), leg("station", "hakone", "train"),
                 leg("hakone", "ryokan", "taxi")],
    },
    "15": {
        "layout": "geo",
        "title": "מפת מסלול האקונה",
        "stops": [
            stop("ryokan", "Aura Tachibana", 35.2289, 139.1028),
            stop("torii", "Heiwa no Torii", 35.2048, 139.0253),
            stop("port", "Moto-Hakone Port", 35.2017, 139.0302),
            stop("togendai", "Togendai", 35.2378, 138.9959),
            stop("owakudani", "Owakudani", 35.2441, 139.0207),
            stop("sounzan", "Sounzan / Gora", 35.2507, 139.0357),
            stop("museum", "Open-Air Museum", 35.2458, 139.0508),
        ],
        "legs": [leg("ryokan", "torii", "bus"), leg("torii", "port", "walk"),
                 leg("port", "togendai", "ship"), leg("togendai", "owakudani", "ropeway"),
                 leg("owakudani", "sounzan", "ropeway"), leg("sounzan", "museum", "train"),
                 leg("museum", "ryokan", "train")],
    },
    "18": {
        "layout": "geo",
        "title": "מפת מסלול היגשיאמה וגיון",
        "stops": [
            stop("hotel", "Hotel Monterey", 35.0078, 135.7593),
            stop("mimosa", "Mimosa / Yasaka Pagoda", 34.9987, 135.7793),
            stop("kiyomizu", "Kiyomizu-dera", 34.9949, 135.7850),
            stop("kodaiji", "Kodai-ji", 35.0007, 135.7813),
            stop("kenninji", "Kennin-ji", 35.0001, 135.7734),
            stop("gion", "Yasaka Shrine / Gion", 35.0037, 135.7786),
            stop("pontocho", "Pontocho", 35.0052, 135.7707),
        ],
        "legs": [leg("hotel", "mimosa", "taxi"), leg("mimosa", "kiyomizu", "walk"),
                 leg("kiyomizu", "kodaiji", "walk"), leg("kodaiji", "kenninji", "walk"),
                 leg("kenninji", "gion", "walk"), leg("gion", "pontocho", "walk")],
    },
    "19": {
        "layout": "geo",
        "title": "מפת מסלול אראשיאמה וצפון קיוטו",
        "stops": [
            stop("hotel", "Hotel Monterey", 35.0078, 135.7593),
            stop("bamboo", "Bamboo Grove", 35.0170, 135.6713),
            stop("tenryuji", "Tenryu-ji", 35.0158, 135.6737),
            stop("bridge", "Togetsukyo / Hogon-in", 35.0136, 135.6778),
            stop("ryoanji", "Ryoan-ji", 35.0345, 135.7183),
            stop("kinkakuji", "Kinkaku-ji", 35.0394, 135.7292),
            stop("kitano", "Kitano Tenmangu", 35.0312, 135.7351),
        ],
        "legs": [leg("hotel", "bamboo", "train"), leg("bamboo", "tenryuji", "walk"),
                 leg("tenryuji", "bridge", "walk"), leg("bridge", "ryoanji", "train"),
                 leg("ryoanji", "kinkakuji", "taxi"), leg("kinkakuji", "kitano", "taxi")],
    },
    "20": {
        "layout": "geo",
        "title": "מפת מסלול קיוטו, נארה ואוסקה",
        "stops": [
            stop("hotel", "Hotel Monterey", 35.0078, 135.7593),
            stop("fushimi", "Fushimi Inari", 34.9671, 135.7727),
            stop("nara", "Nara Park", 34.6850, 135.8430),
            stop("todaiji", "Todai-ji", 34.6890, 135.8398),
            stop("kasuga", "Kasuga Taisha", 34.6814, 135.8484),
            stop("kintetsu", "Kintetsu-Nara", 34.6844, 135.8275),
            stop("osaka", "Villa Fontaine Umeda", 34.7017, 135.5001),
        ],
        "legs": [leg("hotel", "fushimi", "metro"), leg("fushimi", "nara", "train"),
                 leg("nara", "todaiji", "walk"), leg("todaiji", "kasuga", "walk"),
                 leg("kasuga", "kintetsu", "walk"), leg("kintetsu", "osaka", "train")],
    },
    "21": {
        "layout": "geo",
        "title": "מפת מסלול אומדה ונמבה",
        "stops": [
            stop("hotel1", "Villa Fontaine Umeda", 34.7017, 135.5001),
            stop("sky", "Umeda Sky Building", 34.7053, 135.4900),
            stop("kuromon", "Kuromon Market", 34.6654, 135.5065),
            stop("shinsekai", "Shinsekai", 34.6525, 135.5063),
            stop("yasaka", "Namba Yasaka", 34.6625, 135.4961),
            stop("dotonbori", "Dotonbori / Hozenji", 34.6687, 135.5013),
            stop("hotel2", "Osaka Excel Hotel", 34.6806, 135.5008),
        ],
        "legs": [leg("hotel1", "sky", "walk"), leg("sky", "kuromon", "metro"),
                 leg("kuromon", "shinsekai", "metro"), leg("shinsekai", "yasaka", "metro"),
                 leg("yasaka", "dotonbori", "walk"), leg("dotonbori", "hotel2", "metro")],
    },
    "22": {
        "layout": "geo",
        "title": "מפת מסלול טירת אוסקה וטנוג'י",
        "stops": [
            stop("castle", "Osaka Castle", 34.6873, 135.5262),
            stop("shitennoji", "Shitennoji", 34.6546, 135.5165),
            stop("garden", "Keitakuen Garden", 34.6513, 135.5116),
            stop("harukas", "Abeno Harukas 300", 34.6461, 135.5133),
            stop("teamlab", "teamLab Botanical", 34.6102, 135.5200),
            stop("namba", "Namba / Dotonbori", 34.6687, 135.5013),
        ],
        "legs": [leg("castle", "shitennoji", "metro"),
                 leg("shitennoji", "garden", "walk"), leg("garden", "harukas", "walk"),
                 leg("harukas", "teamlab", "metro"), leg("teamlab", "namba", "metro")],
    },
    "23": {
        "layout": "geo",
        "title": "מפת מסלול פסטיבל וסומיושי",
        "stops": [
            stop("festival", "Shinno-sai Festival", 34.6886, 135.5067),
            stop("namba", "Nankai Namba", 34.6636, 135.5019),
            stop("sumiyoshi", "Sumiyoshi Taisha", 34.6128, 135.4929),
            stop("shinsaibashi", "Shinsaibashi", 34.6750, 135.5010),
            stop("dotonbori", "Dotonbori", 34.6687, 135.5013),
        ],
        "legs": [leg("festival", "namba", "metro"),
                 leg("namba", "sumiyoshi", "train"), leg("sumiyoshi", "namba", "train"),
                 leg("namba", "shinsaibashi", "walk"), leg("shinsaibashi", "dotonbori", "walk")],
    },
    "24": {
        "layout": "geo",
        "title": "מפת מסלול אוסקה לטוקיו",
        "stops": [
            stop("hotel", "Osaka Excel Hotel", 34.6806, 135.5008),
            stop("shin_osaka", "Shin-Osaka", 34.7335, 135.5002),
            stop("tokyo", "Tokyo Station", 35.6812, 139.7671),
            stop("tsukishima", "Tsukishima", 35.6649, 139.7847),
            stop("ginza", "Nissan / Ginza Six", 35.6697, 139.7642),
            stop("remm", "remm PLUS Ginza", 35.6672, 139.7621),
            stop("dinner", "Akita Dining Namahage", 35.6694, 139.7624),
        ],
        "legs": [leg("hotel", "shin_osaka", "metro"), leg("shin_osaka", "tokyo", "shinkansen"),
                 leg("tokyo", "tsukishima", "metro"), leg("tsukishima", "ginza", "metro"),
                 leg("ginza", "remm", "walk"), leg("remm", "dinner", "walk")],
    },
    "25": {
        "layout": "geo",
        "title": "מפת מסלול הראג'וקו ושיבויה",
        "stops": [
            stop("meiji", "Meiji Jingu", 35.6764, 139.6993),
            stop("takeshita", "Takeshita Street", 35.6715, 139.7030),
            stop("omotesando", "Omotesando / Cat Street", 35.6673, 139.7088),
            stop("parco", "Shibuya PARCO", 35.6620, 139.6987),
            stop("sky", "Shibuya Sky", 35.6585, 139.7022),
            stop("crossing", "Hachiko / Crossing", 35.6595, 139.7005),
            stop("nonbei", "Nonbei Yokocho", 35.6606, 139.7017),
        ],
        "legs": [leg("meiji", "takeshita", "walk"), leg("takeshita", "omotesando", "walk"),
                 leg("omotesando", "parco", "walk"), leg("parco", "sky", "walk"),
                 leg("sky", "crossing", "walk"), leg("crossing", "nonbei", "walk")],
    },
    "26": {
        "layout": "geo",
        "title": "מפת מסלול צוקיג'י, אזאבודאי וגינזה",
        "stops": [
            stop("tsukiji", "Tsukiji Market", 35.6655, 139.7707),
            stop("azabudai", "teamLab / Azabudai Hills", 35.6605, 139.7404),
            stop("ginza", "Ginza Shopping", 35.6717, 139.7649),
            stop("hotel", "remm PLUS Ginza", 35.6672, 139.7621),
        ],
        "legs": [leg("tsukiji", "azabudai", "metro"), leg("azabudai", "ginza", "metro"),
             leg("ginza", "hotel", "walk")],
    },
    "27": {
        "layout": "geo",
        "title": "מפת מסלול אסאקוסה, אקיהברה ואואנו",
        "stops": [
            stop("sensoji", "Senso-ji / Nakamise", 35.7148, 139.7967),
            stop("akihabara", "Akihabara", 35.6984, 139.7731),
            stop("ueno", "Ueno Park", 35.7148, 139.7732),
            stop("ameyoko", "Ameyoko Market", 35.7101, 139.7746),
            stop("ginza", "Ginza Hotel / Dinner", 35.6694, 139.7635),
        ],
        "legs": [leg("sensoji", "akihabara", "metro"), leg("akihabara", "ueno", "metro"),
                 leg("ueno", "ameyoko", "walk"), leg("ameyoko", "ginza", "metro")],
    },
    "28": {
        "layout": "geo",
        "title": "מפת מסלול טוקיו והטיסה הביתה",
        "stops": [
            stop("hotel", "remm PLUS Ginza", 35.6672, 139.7621),
            stop("zojoji", "Zojo-ji", 35.6575, 139.7483),
            stop("tower", "Tokyo Tower", 35.6586, 139.7454),
            stop("nrt", "Narita Airport", 35.7720, 140.3929),
            stop("auh", "Abu Dhabi Airport", 24.4330, 54.6511),
            stop("tlv", "Ben Gurion Airport", 32.0055, 34.8854),
        ],
        "legs": [leg("hotel", "zojoji", "metro"), leg("zojoji", "tower", "walk"),
                 leg("tower", "nrt", "train"), leg("nrt", "auh", "flight"), leg("auh", "tlv", "flight")],
    },
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


def geo_view(stops):
    lats = [item["lat"] for item in stops]
    lons = [item["lon"] for item in stops]
    lat_pad = max((max(lats) - min(lats)) * 0.22, 0.0025)
    lon_pad = max((max(lons) - min(lons)) * 0.16, 0.0035)
    bounds = (min(lons) - lon_pad, min(lats) - lat_pad, max(lons) + lon_pad, max(lats) + lat_pad)
    west, south, east, north = bounds
    for zoom in range(17, 8, -1):
        left, top = world_pixel(north, west, zoom)
        right, bottom = world_pixel(south, east, zoom)
        if right - left <= WIDTH * 1.15 and bottom - top <= MAP_HEIGHT * 1.15:
            return bounds, zoom
    return bounds, 9


def tile_image(zoom, tile_x, tile_y):
    os.makedirs(TILE_CACHE, exist_ok=True)
    path = os.path.join(TILE_CACHE, f"{zoom}_{tile_x}_{tile_y}.png")
    if not os.path.exists(path):
        url = f"https://tile.openstreetmap.org/{zoom}/{tile_x}/{tile_y}.png"
        request = urllib.request.Request(url, headers={"User-Agent": "Japan2026TripMap/1.0"})
        with urllib.request.urlopen(request) as response:
            payload = response.read()
        with open(path, "wb") as handle:
            handle.write(payload)
    return Image.open(path).convert("RGB")


def base_map(stops):
    bounds, zoom = geo_view(stops)
    west, south, east, north = bounds
    left, top = world_pixel(north, west, zoom)
    right, bottom = world_pixel(south, east, zoom)
    x0, y0 = int(left // 256), int(top // 256)
    x1, y1 = int(right // 256), int(bottom // 256)
    mosaic = Image.new("RGB", ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    for tile_x in range(x0, x1 + 1):
        for tile_y in range(y0, y1 + 1):
            mosaic.paste(tile_image(zoom, tile_x, tile_y), ((tile_x - x0) * 256, (tile_y - y0) * 256))
    crop = (round(left - x0 * 256), round(top - y0 * 256), round(right - x0 * 256), round(bottom - y0 * 256))
    image = mosaic.crop(crop).resize((WIDTH, MAP_HEIGHT), Image.Resampling.LANCZOS)

    def project(item):
        x = (world_pixel(item["lat"], item["lon"], zoom)[0] - left) / (right - left) * WIDTH
        y = (world_pixel(item["lat"], item["lon"], zoom)[1] - top) / (bottom - top) * MAP_HEIGHT
        return round(x), round(y + TITLE_HEIGHT)

    return image, project


def schematic_base(stops):
    image = Image.new("RGB", (WIDTH, MAP_HEIGHT), (242, 246, 250))
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 60):
        draw.line((x, 0, x, MAP_HEIGHT), fill=(226, 232, 240), width=1)
    for y in range(0, MAP_HEIGHT, 60):
        draw.line((0, y, WIDTH, y), fill=(226, 232, 240), width=1)
    count = len(stops)
    columns = 4 if count >= 7 else 3
    top_count = min(columns, count)
    bottom_count = count - top_count
    positions = {}
    top_x = [110 + index * (680 / max(top_count - 1, 1)) for index in range(top_count)]
    for index in range(top_count):
        positions[stops[index]["key"]] = (round(top_x[index]), TITLE_HEIGHT + 145)
    if bottom_count:
        bottom_x = [110 + index * (680 / max(bottom_count - 1, 1)) for index in range(bottom_count)]
        bottom_x.reverse()
        for index in range(bottom_count):
            positions[stops[top_count + index]["key"]] = (round(bottom_x[index]), TITLE_HEIGHT + 340)
    return image, lambda item: positions[item["key"]]


def label_box(draw, center, text, text_font):
    box = draw.textbbox(center, text, font=text_font, anchor="mm")
    return (box[0] - 10, box[1] - 7, box[2] + 10, box[3] + 7)


def boxes_overlap(first, second, gap=4):
    return not (
        first[2] + gap < second[0] or first[0] > second[2] + gap
        or first[3] + gap < second[1] or first[1] > second[3] + gap
    )


def marker_box(point, radius=27):
    x, y = point
    return (x - radius, y - radius, x + radius, y + radius)


def spread_marker_points(points):
    keys = list(points)
    adjusted = {key: [float(points[key][0]), float(points[key][1])] for key in keys}
    minimum_distance = 66.0
    for iteration in range(160):
        changed = False
        for first_index, first_key in enumerate(keys):
            for second_index in range(first_index + 1, len(keys)):
                second_key = keys[second_index]
                first = adjusted[first_key]
                second = adjusted[second_key]
                dx, dy = second[0] - first[0], second[1] - first[1]
                distance = math.hypot(dx, dy)
                if distance >= minimum_distance:
                    continue
                if distance < 0.1:
                    angle = (first_index + second_index + 1) * math.pi / 4
                    dx, dy, distance = math.cos(angle), math.sin(angle), 1.0
                push = (minimum_distance - distance) / 2 + 0.5
                ux, uy = dx / distance, dy / distance
                first[0] -= ux * push
                first[1] -= uy * push
                second[0] += ux * push
                second[1] += uy * push
                changed = True
        for value in adjusted.values():
            value[0] = max(31, min(WIDTH - 31, value[0]))
            value[1] = max(TITLE_HEIGHT + 31, min(TITLE_HEIGHT + MAP_HEIGHT - 31, value[1]))
        if not changed:
            break
    result = {key: (round(value[0]), round(value[1])) for key, value in adjusted.items()}
    boxes = [marker_box(result[key]) for key in keys]
    for first_index, first in enumerate(boxes):
        for second in boxes[first_index + 1:]:
            if boxes_overlap(first, second, gap=6):
                raise RuntimeError("Unable to separate crowded numbered markers")
    return result


def draw_marker(draw, point, number):
    x, y = point
    marker_radius = 27
    marker_color = (30, 41, 79)
    draw.ellipse((x - marker_radius, y - marker_radius, x + marker_radius, y + marker_radius), fill="white", outline=marker_color, width=6)
    draw.text((x, y), str(number), font=font(27, True), fill=marker_color, anchor="mm")


def draw_stop_label(draw, point, label, occupied, marker_boxes, prefer_above):
    x, y = point
    text_font = font(27, True)
    candidates = []
    for radius in (64, 105, 150, 205, 260):
        for angle in (-90, 90, -45, -135, 45, 135, 0, 180):
            radians = math.radians(angle)
            candidates.append((round(math.cos(radians) * radius), round(math.sin(radians) * radius)))
    if not prefer_above:
        candidates[0], candidates[1] = candidates[1], candidates[0]
    chosen = None
    for offset_x, offset_y in candidates:
        center = (x + offset_x, y + offset_y)
        box = label_box(draw, center, label, text_font)
        inside = box[0] >= 4 and box[2] <= WIDTH - 4 and box[1] >= TITLE_HEIGHT + 3 and box[3] <= TITLE_HEIGHT + MAP_HEIGHT - 3
        blockers = occupied + marker_boxes
        clear = all(not boxes_overlap(box, old) for old in blockers)
        if inside and clear:
            chosen = (center, box)
            break
    if chosen is None:
        raise RuntimeError(f"No collision-free label position for {label}")
    center, box = chosen
    draw.rounded_rectangle(box, radius=9, fill=(255, 255, 255, 244), outline=(180, 191, 209), width=2)
    draw.text(center, label, font=text_font, fill=(24, 31, 48), anchor="mm")
    occupied.append(box)


def draw_legend(draw, modes):
    top = TITLE_HEIGHT + MAP_HEIGHT
    draw.rectangle((0, top, WIDTH, TOTAL_HEIGHT), fill=(248, 250, 252))
    rows = [modes] if len(modes) <= 3 else [modes[:3], modes[3:]]
    for row_index, row in enumerate(rows):
        y = top + 28 + row_index * 38
        spacing = WIDTH / len(row)
        for index, mode in enumerate(row):
            color, label = MODE_STYLES[mode]
            x = round(spacing * index + spacing / 2 - 70)
            draw.line((x, y, x + 44, y), fill=color, width=9)
            draw.text((x + 56, y), he(label), font=font(20, True), fill=(35, 41, 54), anchor="lm")
    draw.text((WIDTH - 10, TOTAL_HEIGHT - 10), "© OpenStreetMap contributors", font=font(11), fill=(90, 98, 112), anchor="rm")


def build_day(day):
    config = DAY_MAPS[day]
    stops = config["stops"]
    if config["layout"] == "geo":
        background, project = base_map(stops)
    else:
        background, project = schematic_base(stops)
    card = Image.new("RGB", (WIDTH, TOTAL_HEIGHT), "white")
    card.paste(background, (0, TITLE_HEIGHT))
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, WIDTH, TITLE_HEIGHT), fill=(30, 41, 79))
    draw.text((WIDTH // 2, TITLE_HEIGHT // 2), he(config["title"]), font=font(27, True), fill="white", anchor="mm")
    by_key = {item["key"]: item for item in stops}
    route_points = {key: project(item) for key, item in by_key.items()}
    points = spread_marker_points(route_points)
    used_modes = []
    for start, end, mode in config["legs"]:
        if mode not in used_modes:
            used_modes.append(mode)
        color = MODE_STYLES[mode][0]
        draw.line((route_points[start], route_points[end]), fill="white", width=17)
        draw.line((route_points[start], route_points[end]), fill=color, width=10)
    for key, route_point in route_points.items():
        marker_point = points[key]
        if math.dist(route_point, marker_point) > 5:
            draw.line((route_point, marker_point), fill="white", width=7)
            draw.line((route_point, marker_point), fill=(71, 85, 105), width=3)
    all_marker_boxes = [marker_box(points[item["key"]]) for item in stops]
    for index, item in enumerate(stops, start=1):
        draw_marker(draw, points[item["key"]], index)
    occupied = []
    for index, item in enumerate(stops, start=1):
        x, y = points[item["key"]]
        draw_stop_label(
            draw, (x, y), item["label"], occupied, all_marker_boxes,
            prefer_above=(index % 2 == 1),
        )
    draw_legend(draw, used_modes)
    output = os.path.join("assets", "maps", f"day{day.replace('-', '_')}_route_map.png")
    card.save(output, optimize=True)
    print("saved", output, card.size)
    return output


def contact_sheet(paths):
    thumbs = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((450, 300), Image.Resampling.LANCZOS)
        thumbs.append((path, image.copy()))
    rows = math.ceil(len(thumbs) / 2)
    sheet = Image.new("RGB", (920, rows * 330), (230, 234, 240))
    draw = ImageDraw.Draw(sheet)
    for index, (path, image) in enumerate(thumbs):
        x = (index % 2) * 460 + 5
        y = (index // 2) * 330 + 25
        sheet.paste(image, (x, y))
        draw.text((x + 5, 8 + (index // 2) * 330), os.path.basename(path), font=font(16, True), fill=(25, 30, 45))
    output = os.path.join("assets", "maps", "_all_days_contact_sheet.jpg")
    sheet.save(output, quality=88)
    print("saved", output, sheet.size)


if __name__ == "__main__":
    selected = sys.argv[1:] or list(DAY_MAPS)
    generated = [build_day(day) for day in selected]
    if len(generated) > 1:
        contact_sheet(generated)