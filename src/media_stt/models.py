"""Domain models shared by every transcription backend."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Segment:
    """A transcribed span with start/end times in seconds."""

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Transcription:
    text: str
    language: str
    segments: list[Segment] = field(default_factory=list)
    elapsed_seconds: float = 0.0
