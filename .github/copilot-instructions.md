# Copilot Instructions — Japan 2026 Trip App

## Language rules
- The app UI language is **Hebrew (RTL)**. English is allowed only for place names,
  attraction names, and addresses.
- **Never leave Russian text in the app or its assets.** The planning source images
  (`prep_days/`, `updated_days/`) are in Russian — whenever you bring any of their
  content into the app (titles, themes, legends, labels, notes, timeline text, etc.),
  **translate it to Hebrew**.
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
- Per-day route maps are extracted from `updated_days/DD_11_2026.jpeg` into
  `assets/maps/dayDD_route_map.png` and registered in `routeMapsByDay`.
