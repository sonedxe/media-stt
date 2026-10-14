"""Tests for :mod:`media_stt.writers`."""

from __future__ import annotations

from pathlib import Path

from media_stt.transcriber import Segment, Transcription
from media_stt.writers import render_metadata, render_srt, write_srt


def test_render_srt_formats_segments() -> None:
    segments = [Segment(start=0.0, end=2.5, text="Hola"), Segment(start=2.5, end=4.0, text="Mundo")]

    document = render_srt(segments)

    assert document.startswith("1\n00:00:00,000 --> 00:00:02,500\nHola")
    assert "2\n00:00:02,500 --> 00:00:04,000\nMundo" in document


def test_render_metadata_includes_key_fields() -> None:
    transcription = Transcription(text="hola", language="es", elapsed_seconds=61)
    report = render_metadata(transcription, Path("note.opus"), "test-model")

    assert "note.opus" in report
    assert "test-model" in report
    assert "es" in report
    assert "01:01" in report
    assert "Characters:\n4" in report


def test_write_srt_creates_file(tmp_path: Path) -> None:
    target = tmp_path / "out.srt"
    write_srt([Segment(start=0.0, end=1.0, text="uno")], target)

    assert target.read_text(encoding="utf-8").startswith("1\n")
