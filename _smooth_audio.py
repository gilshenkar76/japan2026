"""Build clean Russian narration from separately rendered semantic segments."""
from __future__ import annotations

import pathlib
import subprocess
import tempfile
import wave
import hashlib
import os
from collections.abc import Sequence

from gtts import gTTS
import imageio_ffmpeg


SAMPLE_RATE = 44_100
SHORT_PAUSE_SECONDS = 0.24
FULL_PAUSE_SECONDS = 0.48
SPEECH_RATE = 1.08
CACHE_DIR = pathlib.Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "japan2026-audio-cache"


def _silence_frames(seconds: float) -> bytes:
    return b"\x00\x00" * int(SAMPLE_RATE * seconds)


def render_segments(
    segments: Sequence[str | tuple[str, str]],
    output_path: str | pathlib.Path,
) -> pathlib.Path:
    """Render segments and join them with explicit short or full pauses."""
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output = pathlib.Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = pathlib.Path(temp_dir)
        pcm_chunks: list[bytes] = []

        for index, item in enumerate(segments):
            if isinstance(item, tuple):
                text, pause_name = item
            else:
                text, pause_name = item, "full"
            cache_key = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
            raw_path = CACHE_DIR / f"{cache_key}.mp3"
            wav_path = temp_root / f"clean-{index:03d}.wav"
            if not raw_path.exists():
                download_path = temp_root / f"raw-{index:03d}.mp3"
                gTTS(text.strip(), lang="ru", slow=False).save(str(download_path))
                download_path.replace(raw_path)
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-i",
                    str(raw_path),
                    "-af",
                    "silenceremove=start_periods=1:start_duration=0.03:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_duration=0.03:start_threshold=-42dB,areverse",
                    "-ar",
                    str(SAMPLE_RATE),
                    "-ac",
                    "1",
                    "-c:a",
                    "pcm_s16le",
                    str(wav_path),
                ],
                check=True,
                capture_output=True,
            )
            with wave.open(str(wav_path), "rb") as wav_file:
                pcm_chunks.append(wav_file.readframes(wav_file.getnframes()))
            pause_seconds = SHORT_PAUSE_SECONDS if pause_name == "short" else FULL_PAUSE_SECONDS
            pcm_chunks.append(_silence_frames(pause_seconds))

        joined_path = temp_root / "joined.wav"
        with wave.open(str(joined_path), "wb") as joined_file:
            joined_file.setnchannels(1)
            joined_file.setsampwidth(2)
            joined_file.setframerate(SAMPLE_RATE)
            joined_file.writeframes(b"".join(pcm_chunks))

        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(joined_path),
                "-af",
                f"loudnorm=I=-18:LRA=7:TP=-2,silenceremove=stop_periods=-1:stop_duration=0.55:stop_threshold=-35dB:stop_silence=0.35,atempo={SPEECH_RATE}",
                "-codec:a",
                "libmp3lame",
                "-b:a",
                "96k",
                str(output),
            ],
            check=True,
            capture_output=True,
        )
    return output
