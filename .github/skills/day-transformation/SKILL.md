---
name: day-transformation
description: 'Transform a Japan 2026 trip-app day (index.html) into the fully "transformed" pattern used by days 14/19/21/23: real cropped local attraction photos, a translated Hebrew route-map image, hotel data, and timeline entries rendered with the shared flexible-height event card (photo-as-nav-link, time badge overlay, 3D hover, pin icon). Use when asked to "transform day X", "apply this layout/pattern to day X", "do day X like day 19/23", "add real photos and map for day X", or any request to bring a day up to the same standard as days 19/21/23 in the japan2026 app.'
---

# Day Transformation Pattern (Japan 2026 app)

## What "transformed" means
A day goes from generic Unsplash-stock timeline events to:
1. Real local cropped photos per attraction (not stock images)
2. A translated Hebrew route-map image (source is Russian — no Russian may ship)
3. Hotel card data (`hotelsByDay`)
4. Timeline events rendered with the **already-global** shared card component — flexible height with a min-height floor, full-height clickable photo with overlaid time badge, 3D hover-lift, pin-icon hint. **Keep the shared CSS/JS behavior exactly as defined below** so all days look identical.
5. Optional extras: theme subtitle, public-transport legs, curated Hebrew route notes.

Days 19, 21, 23 are the reference implementations. Day 14 also uses the shared card but was sourced from the older `prep_days` PNG format (see Prerequisites).

## Shared timeline UI baseline (apply to all days)
These are global style rules for the shared timeline card and must stay consistent when transforming additional days:

- Time badge (`.time-badge`): flush to the image top edge with no margin (`top: 0; left: 0; right: 0; border-radius: 0`).
- Map pin icon (`.event-img-nav::after`): flush to the bottom-right corner (`bottom: 0; right: 0`).
- Timeline image block (`.event-img-nav`, `.event-img-nav img`): keep a uniform baseline width and minimum height (`width: 110px; min-height: 110px`), but do **not** lock it to a fixed height. The image column must stretch to the full card height when the text content is taller than the default baseline.

If a user asks to tune these values, update the shared CSS once in `index.html` and verify it affects all days uniformly (do not add day-specific CSS branches).

- Hotel action buttons (`.hotel .actions > .btn`): keep the hotel CTA row wrapped and responsive. The actions container must allow wrapping, and buttons should use flexible widths so `ניווט`, `Booking`, and copy actions never overflow outside the hotel card on narrow layouts.

## Prerequisites: source image
Look for `updated_days/DD_11_2026.jpeg` — the Russian-original one-page day plan (has a column of small attraction photo thumbnails + a compact route-map card with a title bar and legend).
- **Exists** → follow the workflow below (this is how 19/21/23 were built).
- **Does not exist** (true today for every day except 19/21/23) → check `prep_days/DD.11.2026.png` (older layout, used for day 14's photos originally). Its layout differs — inspect visually first. If neither source is available, ask the user for one before proceeding; do not fabricate photos or map data.

## Step-by-step workflow

### 1. Inspect the source image
Use `view_image` on `updated_days/DD_11_2026.jpeg` (or the `prep_days` PNG) to see the layout. Note the approximate pixel bounding box of:
- The attraction-photo thumbnail column (one box per attraction, stacked vertically)
- The small route-map card (title bar + map + legend), typically bottom-left or bottom-right of the sheet

Always confirm the actual image size in code (`Image.open(SRC).size`) — don't assume dimensions from other days.

### 2. Crop attraction photos → `_crop_dayDD_thumbs.py`
Copy [`_crop_day19_thumbs.py`](../../../_crop_day19_thumbs.py) or [`_crop_day23_thumbs.py`](../../../_crop_day23_thumbs.py) as a template:
```python
"""Crop attraction thumbnails from updated_days/DD_11_2026.jpeg into assets/attractions/dayDD/."""
import os
from PIL import Image

SRC = "updated_days/DD_11_2026.jpeg"
OUT = "assets/attractions/dayDD"
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert("RGB")

boxes = [
    ("slug1", left, top, right, bottom),
    ("slug2", left, top, right, bottom),
    # one row per attraction, same order as the timeline
]
for name, l, t, r, b in boxes:
    im.crop((l, t, r, b)).save(os.path.join(OUT, f"{name}.jpg"), quality=88)
# also build a _contact_sheet.jpg grid for quick visual QA (see day19/23 scripts for the exact pattern)
```
Run with the repo's local venv:
```
& "<repo>\.venv\Scripts\python.exe" _crop_dayDD_thumbs.py
```
Then `view_image` the contact sheet (and any suspicious individual crop) to check for:
- **No white-gap bleed** at the top/bottom edges — if present, nudge the box inward a few px (this was the exact bug fixed on day 19: `eikando` box moved from `(103,138,293,236)` to `(103,129,293,244)`).
- Each photo matches the right attraction/order.

### 3. Build the translated route map → `_build_dayDD_map.py`
Copy [`_build_day19_map.py`](../../../_build_day19_map.py) / [`_build_day21_map.py`](../../../_build_day21_map.py) / [`_build_day23_map.py`](../../../_build_day23_map.py) as a template:
```python
from PIL import Image, ImageDraw, ImageFont

SRC = "updated_days/DD_11_2026.jpeg"
OUT = "assets/maps/dayDD_route_map.png"

im = Image.open(SRC).convert("RGB")
card = im.crop((left, top, right, bottom))  # map card only: title bar + map + legend
d = ImageDraw.Draw(card)

def font(sz):
    for p in (r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()

def he(s):
    # PIL draws LTR; reverse a pure-Hebrew logical string so it renders correctly RTL
    return s[::-1]

# 1) paint a solid rectangle over the Russian title bar, draw Hebrew "מפת מסלול היום" centered
# 2) paint a rectangle over each Russian legend line / parenthetical node label, draw the Hebrew
#    translation with he(...) at the same spot (keep English place names and pins as-is)

card.save(OUT)
```
Common Russian → Hebrew translations needed (see [.github/copilot-instructions.md](../../copilot-instructions.md)):
| Russian | Hebrew |
|---|---|
| Пешком | רגלי |
| Общественный транспорт / Транспорт | תחבורה ציבורית |
| Поезда | רכבת |
| Переезды | נסיעה |
| Вечерний маршрут | מסלול ערב |
| Обед | ארוחת צהריים |
| Ужин | ארוחת ערב |
| (отель) | (מלון) |
| Title bar text | מפת מסלול היום |

Run the script with the same venv python, then `view_image` the output PNG to confirm no Russian text remains and everything is legible.

### 4. Register in `index.html` — data only, never a new render branch
The card rendering is already generic (the default `timeline` branch in the `render(day)` function). **Do not** add a per-day `if (day === 'DD')` rendering branch — only add/extend data objects. Use an existing day (19/21/23) entry as a copy template for each of these (all defined near the top of the script, in this order):

1. **`citiesByDay[day]`** — `{ city: '<Hebrew city name>', image: '<fallback Unsplash url, only used for the main-page day card>' }`. Usually already present for every day 12-28; only add if missing.
2. **`data[day].events`** — array of `[timeStr, title, desc, imgPath, mapsQuery, transitNote?]`.
   - `timeStr` supports `"09:00<br>10:00"` for a start–end range (renders as `09:00 – 10:00`), or a single time string.
   - `imgPath` = the cropped local photo from step 2, e.g. `assets/attractions/dayDD/eikando.jpg`.
   - Insert a section divider row with `["", "__SECTION__", "🍸 section title text", "", ""]` (e.g. between afternoon and evening blocks).
   - `transitNote` (optional 6th field) — short Hebrew line shown under the description, e.g. `"🚶 רגלי ≈ 5 דק׳ מהתחנה"`.
3. **`hotelsByDay[day]`** — `{ name, meta, mapQuery, bookingUrl, bookingAppUrl, extra }` (full address goes in `extra`). Copy from an adjacent day if the hotel spans multiple days.
4. **`routeMapsByDay[day]`** *(optional but recommended once a translated map exists)* — `{ src: 'assets/maps/dayDD_route_map.png', ratio: '<cropWidth> / <cropHeight>', legend: false }`. `legend:false` because the legend text is already baked into the image.
5. **`themesByDay[day]`** *(optional)* — short Hebrew subtitle shown under the big city name in the day banner.
6. **`transitByDay[day]`** *(optional)* — array of `{ from, to, note, line, time, cost }` legs shown on the תחבורה tab.
7. **`routeNotesPresets[day]`** *(optional)* — `{ overview, tips }` Hebrew text prefilled into the day's notes box.

### 5. Verify in the browser
Reload `index.html` and navigate to the day. Element refs go stale after a reload, so re-query each time, e.g.:
```js
document.querySelector(`[onclick="showDayPlanFromMain('DD')"]`)?.click()
```
Check: photos load correctly, **no Russian text anywhere**, card heights flex with content but share a consistent ~90px+ floor, the route map renders with the correct aspect ratio and translated legend, and the hotel card shows correct info.

### 6. Commit & push
This repo commits straight to `master` (no feature-branch workflow) — `git add`, a descriptive commit message, `git push`.

## Key facts / gotchas
- The event-card CSS/JS (`.event`, `.event-img-nav`, `.event-content`, `.time-badge`, 3D hover, pin icon) lives once in the shared `render(day)` default branch — it already applies to every day. Never duplicate it per day.
- This repo's Python env: `.venv\Scripts\python.exe` inside the workspace root (activate via `.venv\Scripts\Activate.ps1` if needed).
- Source jpegs currently only exist for days 19/21/23 (`updated_days/`). Every other day only has the older `prep_days/DD.11.2026.png` — inspect it before reusing any crop-box numbers from another day.
- Crop boxes are unique per source image; there is no universal pixel offset. Always inspect with `view_image` first, crop, then re-check the output before wiring it into `index.html`.
- Never ship Russian text in the app or its assets — translate everything per [.github/copilot-instructions.md](../../copilot-instructions.md).
