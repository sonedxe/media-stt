"""The backend port: anything that turns an audio file into a Transcription."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from media_stt.models import Transcription


class Backend(Protocol):
    """Transcription engine contract.

    Implementations receive audio already decoded to 16 kHz mono WAV.
    """

    name: str
    model: str

    def transcribe(self, audio_path: Path) -> Transcription: ...
