"""Tests for :mod:`media_stt.utils`."""

from __future__ import annotations

from media_stt.utils import format_duration, format_srt_timestamp


def test_format_duration_under_an_hour() -> None:
    assert format_duration(0) == "00:00"
    assert format_duration(65) == "01:05"
    assert format_duration(59.6) == "01:00"


def test_format_duration_with_hours() -> None:
    assert format_duration(3661) == "1:01:01"


def test_format_srt_timestamp() -> None:
    assert format_srt_timestamp(0) == "00:00:00,000"
    assert format_srt_timestamp(2.5) == "00:00:02,500"
    assert format_srt_timestamp(3661.25) == "01:01:01,250"
