"""Thin, testable wrapper around Whisper MLX."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Segment:
    """A transcribed span with start/end times in seconds."""

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Transcription:
    """The result of transcribing a single file."""

    text: str
    language: str
    segments: list[Segment] = field(default_factory=list)
    elapsed_seconds: float = 0.0


class Transcriber:
    """Transcribe audio files locally with Whisper MLX."""

    def __init__(self, model: str, language: str | None = None) -> None:
        self.model = model
        self.language = language

    def transcribe(self, audio_path: Path) -> Transcription:
        """Transcribe ``audio_path`` and return the decoded result."""
        # Imported lazily so the rest of the package stays importable (and
        # testable) on machines without MLX.
        import mlx_whisper

        started = time.perf_counter()
        result = mlx_whisper.transcribe(
            str(audio_path),
            path_or_hf_repo=self.model,
            language=self.language,
            verbose=False,
        )
        elapsed = time.perf_counter() - started

        segments = [
            Segment(
                start=float(segment["start"]),
                end=float(segment["end"]),
                text=str(segment["text"]).strip(),
            )
            for segment in result.get("segments", [])
        ]
        return Transcription(
            text=str(result["text"]).strip(),
            language=str(result.get("language", "unknown")),
            segments=segments,
            elapsed_seconds=elapsed,
        )
