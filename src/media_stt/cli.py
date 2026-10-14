"""Command-line interface for Media STT."""

from __future__ import annotations

import argparse
import logging
from collections.abc import Iterator
from pathlib import Path

from tqdm import tqdm

from media_stt import __version__
from media_stt.audio import AudioError, ensure_ffmpeg
from media_stt.backends import BackendError, create_backend, supported_backends
from media_stt.config import DEFAULT_OUTPUT_DIR
from media_stt.discovery import collect_inputs
from media_stt.pipeline import FileOutcome, Pipeline
from media_stt.utils import format_duration

logger = logging.getLogger("media_stt")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="media-stt",
        description="Local speech-to-text powered by Whisper (MLX or faster-whisper).",
    )
    parser.add_argument(
        "audio",
        nargs="+",
        help="Audio/video file(s) or directory(ies) to transcribe",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "-b",
        "--backend",
        choices=supported_backends(),
        default=None,
        help="Transcription backend (default: auto by platform)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=None,
        help="Model name or Hugging Face repo (default: backend-specific)",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="auto",
        help="Force language, e.g. es or en (default: auto-detect)",
    )
    parser.add_argument(
        "--srt",
        action="store_true",
        help="Also write a .srt subtitle file with timestamps",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Scan directories recursively",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show debug logging",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = build_parser().parse_args(argv)
    _configure_logging(args.verbose)

    try:
        ensure_ffmpeg()
    except AudioError as error:
        logger.error("%s", error)
        return 1

    sources = collect_inputs(args.audio, recursive=args.recursive)
    if not sources:
        logger.error("Nothing to transcribe.")
        return 1

    language = None if args.language.lower() == "auto" else args.language
    output_dir = Path(args.output).expanduser()

    try:
        backend = create_backend(args.backend, args.model, language)
    except BackendError as error:
        logger.error("%s", error)
        return 1

    _print_header(len(sources), backend.name, backend.model, args.language, output_dir)

    pipeline = Pipeline(backend, output_dir, write_subtitles=args.srt)

    results: Iterator[FileOutcome] = pipeline.iter_run(sources)
    if len(sources) > 1:
        results = tqdm(results, total=len(sources), desc="Transcribing", unit="file")

    outcomes = _consume(results)
    failed = sum(not outcome.ok for outcome in outcomes)

    print()
    if failed:
        print(f"⚠️  Finished with errors: {len(outcomes) - failed}/{len(outcomes)} succeeded.")
    else:
        print(f"✅ Completed: {len(outcomes)} file(s).")
    print()
    return 1 if failed else 0


def _consume(results: Iterator[FileOutcome]) -> list[FileOutcome]:
    """Print each outcome as it arrives and collect them for the summary."""
    outcomes: list[FileOutcome] = []
    for outcome in results:
        _print_outcome(outcome)
        outcomes.append(outcome)
    return outcomes


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format="%(message)s")


def _print_header(count: int, backend: str, model: str, language: str, output_dir: Path) -> None:
    print("\n🎙️  Media STT")
    print("-----------------------------")
    print(f"Files   : {count}")
    print(f"Backend : {backend}")
    print(f"Model   : {model}")
    print(f"Language: {language}")
    print(f"Output  : {output_dir}")
    print("-----------------------------")


def _print_outcome(outcome: FileOutcome) -> None:
    if not outcome.ok or outcome.transcription is None:
        print(f"  ❌ {outcome.source.name}: {outcome.error}")
        return

    transcription = outcome.transcription
    print(f"\n🎥 {outcome.source.name}")
    for output in outcome.outputs:
        print(f"  ✅ {output}")
    print(
        f"     language: {transcription.language}"
        f" | time: {format_duration(transcription.elapsed_seconds)}"
        f" | chars: {len(transcription.text)}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
