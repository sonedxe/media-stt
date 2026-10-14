"""Tests for :mod:`media_stt.discovery`."""

from __future__ import annotations

from pathlib import Path

from media_stt.discovery import collect_inputs


def test_collects_media_files_from_directory(tmp_path: Path) -> None:
    (tmp_path / "note.opus").write_bytes(b"x")
    (tmp_path / "song.mp3").write_bytes(b"x")
    (tmp_path / "notes.txt").write_text("ignore me")

    assert collect_inputs([str(tmp_path)]) == [
        tmp_path / "note.opus",
        tmp_path / "song.mp3",
    ]


def test_accepts_explicit_files(tmp_path: Path) -> None:
    audio = tmp_path / "voice.m4a"
    audio.write_bytes(b"x")

    assert collect_inputs([str(audio)]) == [audio]


def test_skips_missing_paths(tmp_path: Path) -> None:
    assert collect_inputs([str(tmp_path / "missing.opus")]) == []


def test_directories_are_not_recursive_by_default(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "deep.mp3").write_bytes(b"x")

    assert collect_inputs([str(tmp_path)]) == []
    assert collect_inputs([str(tmp_path)], recursive=True) == [nested / "deep.mp3"]


def test_duplicates_are_removed(tmp_path: Path) -> None:
    audio = tmp_path / "note.opus"
    audio.write_bytes(b"x")

    assert collect_inputs([str(audio), str(audio)]) == [audio]
