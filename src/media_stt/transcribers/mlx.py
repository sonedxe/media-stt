"""Whisper MLX transcriber, for Apple Silicon."""

from __future__ import annotations

import time
from pathlib import Path

from media_stt.models import Segment, Transcription


class MlxTranscriber:
    name = "mlx"

    def __init__(self, model: str, language: str | None = None) -> None:
        self.model = model
        self.language = language

    def transcribe(self, audio_path: Path) -> Transcription:
        # Imported lazily so the package stays importable without MLX.
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
