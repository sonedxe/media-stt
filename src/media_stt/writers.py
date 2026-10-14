"""Persist transcripts to disk (plain text, SRT subtitles and metadata)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from media_stt.models import Segment, Transcription
from media_stt.utils import format_duration, format_srt_timestamp


def render_srt(segments: list[Segment]) -> str:
    blocks: list[str] = []
    for index, segment in enumerate(segments, start=1):
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{format_srt_timestamp(segment.start)} --> {format_srt_timestamp(segment.end)}",
                    segment.text,
                    "",
                ]
            )
        )
    return "\n".join(blocks)


def render_metadata(transcription: Transcription, source: Path, model: str) -> str:
    return f"""
Media STT Report
================

File:
{source.name}

Model:
{model}

Language:
{transcription.language}

Characters:
{len(transcription.text)}

Processing time:
{format_duration(transcription.elapsed_seconds)}

Created:
{datetime.now()}
"""


def write_text(text: str, path: Path) -> None:
    path.write_text(text, encoding="utf-8")


def write_srt(segments: list[Segment], path: Path) -> None:
    path.write_text(render_srt(segments), encoding="utf-8")


def write_metadata(transcription: Transcription, source: Path, model: str, path: Path) -> None:
    path.write_text(render_metadata(transcription, source, model), encoding="utf-8")
