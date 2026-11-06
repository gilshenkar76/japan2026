---
name: russian-trip-audio-guide
description: 'Create or improve Russian spoken audio guides for the Japan 2026 itinerary. Use when asked to add an audio guide, narration, Russian guide, voice guide, or a guide for any attraction, hotel, meal, transfer, neighborhood, or trip day. Research facts, connect each narration to the stops before and after it, generate smooth natural Russian speech, register it in index.html, test playback, and open the interactive app.'
---

# Russian Trip Audio Guide

Act as one professional, friendly Japan guide accompanying the group throughout the entire trip. Each recording is one chapter in a continuous journey, not an isolated encyclopedia entry.

## Guide personality

- Warm, knowledgeable, practical, and calm.
- Speak to the group as companions using natural phrases such as "мы приехали", "обратите внимание", and "завтра нас ждёт".
- Sound like a human guide beside the travelers, not an advertisement or a list of facts.
- Explain Japanese customs without lecturing or exoticizing them.
- Prioritize details useful at that exact moment and location.

## Language boundary

- Spoken narration and generator source text may be Russian.
- Every visible app element remains Hebrew, except established English place names and addresses.
- Never add visible Russian labels, transcripts, maps, notes, or card text.

## Research and continuity

1. Read the complete itinerary day in `index.html`, including `routeNotesPresets`, events, transport, hotel, and adjacent days.
2. Identify what the group has just done, how they arrived, what they need now, and what comes next.
3. Use the venue's official website for current operational facts. Distinguish stable cultural context from changeable prices and hours.
4. Open with one short transition from the preceding stop or journey.
5. Cover the subject's story and significance, what to notice, practical etiquette, and one or two memorable details.
6. Close with a natural transition to the next planned experience or day.

## Script style for smooth TTS

- Target 3 to 5 minutes unless the user specifies otherwise.
- Use short and medium sentences, generally 8 to 18 words.
- Prefer periods and commas. Avoid semicolons, parentheses, em dashes, slash-separated terms, abbreviations, and dense lists.
- Spell out numbers, times, symbols, and foreign terms as they should be pronounced in Russian.
- Do not insert blank lines into the TTS text.
- Avoid consecutive punctuation and sentence fragments that trigger artificial pauses.
- Read the script aloud mentally and rewrite tongue-twisters or awkward case endings.
- Default delivery should feel energetic but unhurried, around 1.12 to 1.16 times the raw fallback speed.

## Generation pattern

Install the pinned generator dependencies when needed:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements-audio.txt
```

1. Prefer `edge_tts` with a natural Russian neural voice and `rate="+12%"`.
2. If Edge TTS is unavailable, generate with `gTTS(..., lang="ru", slow=False)` into a temporary MP3.
3. Normalize fallback speed with `imageio-ffmpeg` using `atempo=1.14`, preserving pitch.
4. Save the final file under `mp3/<exact concise name>.mp3`.
5. Keep the generator script at the repository root as `_gen_<slug>_audio.py`.

## App integration and verification

1. Register the exact event title in `audioMap` in `index.html`.
2. Do not expose a Russian transcript in the UI.
3. Start the local HTTP server; `file://` cannot reliably load MP3 files in the integrated browser.
4. Open the actual interactive app on the relevant day, not a screenshot.
5. Start playback and verify finite duration, advancing current time, no media error, and correct pause/resume behavior.
6. Check the card at mobile width for overflow.
7. Stage only the skill, generator, MP3, and required app changes before publishing.
