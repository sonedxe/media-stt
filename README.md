# Media STT

**Local, cross-platform speech-to-text for any audio or video file.**

[![CI](https://github.com/sonedxe/media-stt/actions/workflows/ci.yml/badge.svg)](https://github.com/sonedxe/media-stt/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#installation)
[![Powered by Whisper](https://img.shields.io/badge/powered%20by-Whisper-black.svg)](https://github.com/openai/whisper)

Point it at a file and get a transcript back — everything runs **offline on your
machine**, no API keys, no uploads. It decodes any format `ffmpeg` understands,
including **WhatsApp voice notes** (`.opus` / `.ogg`), `.m4a`, `.mp3`, `.wav`
and video files such as `.mp4` / `.mkv`.

```console
$ media-stt "WhatsApp Audio 2026-10-14 at 10.56.31.opus" -l es --srt
🎙️  Media STT
-----------------------------
Files       : 1
Transcriber : mlx
Model       : mlx-community/whisper-medium-mlx
Language    : es
Output      : output
-----------------------------
🎥 WhatsApp Audio 2026-10-14 at 10.56.31.opus
  ✅ output/WhatsApp Audio 2026-10-14 at 10.56.31_2026-10-14_11-21-03.txt
  ✅ output/WhatsApp Audio 2026-10-14 at 10.56.31_2026-10-14_11-21-03.srt
  ✅ output/WhatsApp Audio 2026-10-14 at 10.56.31_2026-10-14_11-21-03.meta
     language: es | time: 00:15 | chars: 2291

✅ Completed: 1 file(s).
```

## Features

- 🎧 **Any format** — audio *and* video, normalized through ffmpeg.
- 💬 **WhatsApp ready** — `.opus` / `.ogg` voice notes just work.
- 🖥️ **Cross-platform** — Apple Silicon (MLX), plus Windows / Linux (faster-whisper).
- 🔒 **Fully local** — models run on your machine; nothing leaves it.
- 📝 **Subtitles** — optional `.srt` output with timestamps.
- 📦 **Batch** — pass many files, or a whole directory (`-r` to recurse).
- 🌐 **Auto language detection**, or force one with `--language`.

## Installation

Requires **Python 3.11+** and **[ffmpeg](https://ffmpeg.org/)** on your `PATH`.

```bash
git clone https://github.com/sonedxe/media-stt.git
cd media-stt
python -m venv .venv
```

Activate the virtual environment:

| Platform | Command |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |

Install ffmpeg if you don't have it:

| Platform | Command |
|---|---|
| macOS | `brew install ffmpeg` |
| Debian / Ubuntu | `sudo apt install ffmpeg` |
| Fedora | `sudo dnf install ffmpeg` |
| Windows | `winget install Gyan.FFmpeg` |

Finally:

```bash
pip install -e .
```

The right transcriber is installed automatically for your platform. The Whisper
model is downloaded on first run and cached in `~/.cache/huggingface/hub`, so
later runs work offline.

## Transcribers

Media STT picks a transcriber automatically based on your platform. Override it
with `--transcriber`.

| Platform | Transcriber | Default model |
|---|---|---|
| macOS (Apple Silicon) | `mlx` | `mlx-community/whisper-medium-mlx` |
| Linux · Windows · CPU | `faster-whisper` | `medium` |

Model names differ per transcriber: MLX takes a Hugging Face repo, faster-whisper
takes a size name.

```bash
media-stt note.opus --transcriber mlx -m mlx-community/whisper-large-v3-mlx   # best on Mac
media-stt note.opus --transcriber faster-whisper -m large-v3                 # tiny..large-v3
```

## Usage

```bash
media-stt "voice-note.opus"                     # one file, auto language
media-stt note.opus recording.m4a               # several files
media-stt ~/Downloads/voice-notes -r -l es --srt   # a whole folder, recursive
```

### Options

| Option | Description |
|---|---|
| `audio` | One or more files, or directories to scan |
| `-o`, `--output` | Output directory (default: `output`) |
| `--transcriber` | `mlx` or `faster-whisper` (default: auto by platform) |
| `-m`, `--model` | Model name or Hugging Face repo (default: transcriber-specific) |
| `-l`, `--language` | Force a language, e.g. `es`, `en` (default: `auto`) |
| `--srt` | Also write a `.srt` subtitle file with timestamps |
| `-r`, `--recursive` | Scan directories recursively |
| `-v`, `--verbose` | Show debug logging |
| `--version` | Print the version and exit |

## Output

For every input `<name>.<ext>` the tool writes to the output directory:

- `<name>_<timestamp>.txt` — the plain transcript
- `<name>_<timestamp>.meta` — transcriber, model, detected language, timing
- `<name>_<timestamp>.srt` — only with `--srt`

## Architecture

A small port-and-adapters layout: the transcription engine is a **port**
(`Transcriber`) with one **adapter** per platform, and everything else is wired
by a thin orchestration layer.

```
src/media_stt/
├── cli.py                      # argument parsing and user-facing output
├── config.py                   # constants and per-transcriber defaults
├── models.py                   # domain models (Transcription, Segment)
├── discovery.py                # expand files/directories into a media list
├── audio.py                    # ffmpeg availability + decode to 16 kHz mono WAV
├── pipeline.py                 # orchestration: decode → transcribe → write
├── writers.py                  # render + persist text, SRT and metadata
├── utils.py                    # time formatting helpers
└── transcribers/
    ├── base.py                 # the Transcriber port (Protocol)
    ├── mlx.py                  # Apple Silicon (Whisper MLX)
    ├── faster_whisper.py       # Windows / Linux / CPU (CTranslate2)
    └── __init__.py             # registry + platform-aware selection
```

Data flows one way: `cli` → `pipeline` → (`audio`, `transcriber`, `writers`).
Transcribers are imported lazily, so the package imports and tests run without
any engine installed.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Notes

- First run of a model is slower (download + warm-up).
- A failing file is reported and the batch continues.
- Want the CPU transcriber on Apple Silicon too? `pip install -e ".[cpu]"`.

## License

[MIT](LICENSE) © 2026 sonedxe
