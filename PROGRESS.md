# Japan 2026 - Current Progress

Last updated: 2026-07-12

## What is completed
- Main trip SPA is working on GitHub Pages.
- Day-by-day route content is updated, including first day (12-13) and last day (28).
- Flight status system is implemented with shared backend sync through Supabase Edge Function.
- Transportation tab contains the live flight status board and auto-sync controls.
- First and last day Route screen include dedicated flight status panel with:
  - Original departure/arrival time and terminal
  - Live status and gate
  - Live departure/arrival schedule and terminal
- Route event cards for first/last day show colored status chips (On Time/Delayed/Unknown).
- Route upload panel was moved to bottom of Route screen for all days.

## Backend and infra
- Supabase project linked: ciabjdoqgedpszxngozu
- Edge Function deployed: flight-status-proxy
- Function source: supabase/functions/flight-status-proxy/index.ts
- Required secret in Supabase: AVIATIONSTACK_API_KEY

## Key files
- index.html (main app UI + logic)
- supabase/functions/flight-status-proxy/index.ts (flight API proxy)

## Latest known checkpoint
- Branch: master
- Latest pushed commit at wrap-up: pending new wrap-up commit/tag
