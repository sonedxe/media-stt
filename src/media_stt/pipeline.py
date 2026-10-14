"""Orchestration: decode → transcribe → write, one file at a time."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory

from media_stt.audio import decode_to_wav
from media_stt.models import Transcription
from media_stt.transcribers.base import Transcriber
from media_stt.utils import file_timestamp
from media_stt.writers import write_metadata, write_srt, write_text

logger = logging.getLogger(__name__)


@dataclass
class FileOutcome:
    """Outcome for a single input file."""

    source: Path
    transcription: Transcription | None = None
    outputs: list[Path] = field(default_factory=list)
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


class Pipeline:
    def __init__(
        self,
        transcriber: Transcriber,
        output_dir: Path,
        *,
        write_subtitles: bool = False,
    ) -> None:
        self.transcriber = transcriber
        self.output_dir = output_dir
        self.write_subtitles = write_subtitles

    def run(self, sources: list[Path]) -> list[FileOutcome]:
        return list(self.iter_run(sources))

    def iter_run(self, sources: list[Path]) -> Iterator[FileOutcome]:
        """Yield outcomes as each file finishes, for live progress reporting."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(prefix="media-stt-") as work_dir:
            for source in sources:
                yield self.run_file(source, Path(work_dir))

    def run_file(self, source: Path, work_dir: Path) -> FileOutcome:
        try:
            wav_path = decode_to_wav(source, work_dir)
            transcription = self.transcriber.transcribe(wav_path)
            outputs = self._write_outputs(source, transcription)
            return FileOutcome(source=source, transcription=transcription, outputs=outputs)
        except Exception as error:  # report and keep processing the batch
            logger.error("Failed to transcribe %s: %s", source.name, error)
            return FileOutcome(source=source, error=str(error))

    def _write_outputs(self, source: Path, transcription: Transcription) -> list[Path]:
        stem = f"{source.stem}_{file_timestamp()}"
        outputs: list[Path] = []

        text_path = self.output_dir / f"{stem}.txt"
        write_text(transcription.text, text_path)
        outputs.append(text_path)

        if self.write_subtitles and transcription.segments:
            srt_path = self.output_dir / f"{stem}.srt"
            write_srt(transcription.segments, srt_path)
            outputs.append(srt_path)

        meta_path = self.output_dir / f"{stem}.meta"
        write_metadata(transcription, source, self.transcriber.model, meta_path)
        outputs.append(meta_path)
        return outputs
