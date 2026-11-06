"""Render Russian guide phrases with Silero and explicit pause timing."""
from __future__ import annotations

import pathlib
from collections.abc import Sequence

import numpy as np
import soundfile as sf
import torch


SAMPLE_RATE = 48_000
DEFAULT_SPEAKER = "aidar"
SHORT_PAUSE_SECONDS = 0.16
NORMAL_PAUSE_SECONDS = 0.32

_model = None


def get_model():
    global _model
    if _model is None:
        _model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="v4_ru",
            trust_repo=True,
        )
        _model.to(torch.device("cpu"))
    return _model


def render_phrases(
    phrases: Sequence[str | tuple[str, str]],
    output_path: str | pathlib.Path,
    speaker: str = DEFAULT_SPEAKER,
) -> pathlib.Path:
    """Render phrases; tuple pause names are 'short' or 'normal'."""
    model = get_model()
    chunks: list[np.ndarray] = []
    pause_lengths = {
        "short": int(SAMPLE_RATE * SHORT_PAUSE_SECONDS),
        "normal": int(SAMPLE_RATE * NORMAL_PAUSE_SECONDS),
    }

    for item in phrases:
        if isinstance(item, tuple):
            text, pause_name = item
        else:
            text, pause_name = item, "normal"
        audio = model.apply_tts(
            text=text.strip(),
            speaker=speaker,
            sample_rate=SAMPLE_RATE,
            put_accent=True,
            put_yo=True,
        )
        chunks.append(audio.detach().cpu().numpy())
        chunks.append(np.zeros(pause_lengths[pause_name], dtype=np.float32))

    output = pathlib.Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output, np.concatenate(chunks), SAMPLE_RATE, subtype="PCM_16")
    return output
