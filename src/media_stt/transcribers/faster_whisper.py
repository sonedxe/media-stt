"""faster-whisper (CTranslate2) transcriber, for Windows, Linux and CPU."""

from __future__ import annotations

import time
from pathlib import Path

from media_stt.models import Segment, Transcription


class FasterWhisperTranscriber:
    name = "faster-whisper"

    def __init__(self, model: str, language: str | None = None, device: str = "auto") -> None:
        self.model = model
        self.language = language
        self.device = device
        self._engine = None

    def _load(self):
        # Loaded once per instance; importing lazily keeps the package importable
        # without CTranslate2 installed.
        if self._engine is None:
            from faster_whisper import WhisperModel

            self._engine = WhisperModel(self.model, device=self.device)
        return self._engine

    def transcribe(self, audio_path: Path) -> Transcription:
        engine = self._load()

        started = time.perf_counter()
        segments, info = engine.transcribe(str(audio_path), language=self.language, beam_size=5)
        collected = list(segments)  # the returned generator is lazy
        elapsed = time.perf_counter() - started

        return Transcription(
            text="".join(segment.text for segment in collected).strip(),
            language=getattr(info, "language", None) or "unknown",
            segments=[
                Segment(start=float(segment.start), end=float(segment.end), text=segment.text.strip())
                for segment in collected
            ],
            elapsed_seconds=elapsed,
        )
