"""Shared CLI runner for the per-day Russian audio-guide generators."""
from __future__ import annotations

import pathlib
import sys
import time

from _smooth_audio import render_segments

OUT_DIR = pathlib.Path("mp3")


def run(guides: dict[str, list[str | tuple[str, str]]]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    selected = set(sys.argv[1:])
    for filename, segments in guides.items():
        if selected and filename not in selected:
            continue
        for attempt in range(6):
            try:
                output = render_segments(segments, OUT_DIR / filename)
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(5 * (attempt + 1))
        print(f"Saved: {output} ({output.stat().st_size // 1024} KB)")
