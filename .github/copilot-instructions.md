# Copilot Instructions — Japan 2026 Trip App

## Language rules
- The app UI language is **Hebrew (RTL)**. English is allowed only for place names,
  attraction names, and addresses.
- **Never leave Russian text in the app or its assets.** The planning source images
  (`prep_days/`, `updated_days/`) are in Russian — whenever you bring any of their
  content into the app (titles, themes, legends, labels, notes, timeline text, etc.),
  **translate it to Hebrew**.
- Exception: spoken audio guides may use Russian. Russian narration text may appear
  only in audio-generation scripts and generated audio files; all visible UI,
  maps, labels, notes, and timeline content must remain Hebrew.
- This applies to text baked into extracted map images too: remove/replace Russian
  words (e.g. legends, `(Гион)` → `(גיון)`) rather than shipping them.

### Common Russian → Hebrew reference
- Пешком → רגלי
- Общественный транспорт → תחבורה ציבורית
- Вечерний маршрут → מסלול ערב
- Обед → ארוחת צהריים · Ужин → ארוחת ערב
- День → יום · Возвращение в отель → חזרה למלון
- Гион → גיון

## Project notes
- `index.html` is a single-file SPA (UI + logic + data). Day content lives in the
  `data`, `citiesByDay`, `hotelsByDay`, `routeMapsByDay`, and `themesByDay` objects.
- The day header is a data-driven banner built by `renderDayBanner(day)`.
- `routeNotesPresets[day].overview` is the authoritative full-day Hebrew description
  shown in the read-only `תכנון היום` section. Whenever events, order, timing,
  transport, bookings, meals, or evening plans change, update that overview in the
  same edit and validate it against the complete day timeline.
- Per-day route maps are extracted from `updated_days/DD_11_2026.jpeg` into
  `assets/maps/dayDD_route_map.png` and registered in `routeMapsByDay`.

## Attraction images rule
- Attraction/timeline images must come from the **photo thumbnails in the source
  image** (`updated_days/DD_11_2026.jpeg`), not from Unsplash or other stock URLs.
- Crop each stop's thumbnail into `assets/attractions/dayDD/<name>.jpg` and reference
  those local paths in the day's `events` array (the 4th field of each event).
- Do the same for every future day update: extract the real photos from the source
  image rather than shipping placeholder stock images.
