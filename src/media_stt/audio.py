"""Decode any input format into Whisper-ready PCM using ffmpeg."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from media_stt.config import CHANNELS, SAMPLE_RATE


class AudioError(RuntimeError):
    """Raised when an input cannot be decoded to audio."""


def ensure_ffmpeg() -> None:
    """Raise a helpful error early when ffmpeg is not available."""
    if shutil.which("ffmpeg") is None:
        raise AudioError("ffmpeg was not found in PATH. Install it with: brew install ffmpeg")


def decode_to_wav(source: Path, work_dir: Path) -> Path:
    """Decode any ffmpeg-readable media into a 16 kHz mono PCM WAV file.

    Video streams are dropped, so ``.mp4``/``.mkv`` inputs work as well as
    audio-only files such as WhatsApp ``.opus`` voice notes.
    """
    target = work_dir / f"{source.stem}.wav"
    command = [
        "ffmpeg",
        "-nostdin",
        "-y",
        "-i",
        str(source),
        "-vn",  # drop any video stream
        "-ac",
        str(CHANNELS),  # mono
        "-ar",
        str(SAMPLE_RATE),  # Whisper sample rate
        "-acodec",
        "pcm_s16le",
        str(target),
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        tail = "\n".join(process.stderr.strip().splitlines()[-5:])
        raise AudioError(f"ffmpeg could not decode '{source.name}':\n{tail}")
    return target
