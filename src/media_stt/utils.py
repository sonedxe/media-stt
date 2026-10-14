"""Small, dependency-free helpers shared across the package."""

from __future__ import annotations

from datetime import datetime


def format_duration(seconds: float) -> str:
    """Format a duration as ``MM:SS`` or ``H:MM:SS`` when it exceeds an hour."""
    total = int(round(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_srt_timestamp(seconds: float) -> str:
    """Format a duration as an SRT timestamp (``HH:MM:SS,mmm``)."""
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def file_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
