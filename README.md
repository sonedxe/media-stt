# Media STT

Local speech-to-text powered by **Whisper MLX**, optimized for Apple Silicon.

Transcribes any audio or video format that `ffmpeg` can decode — including
**WhatsApp voice notes** (`.opus` / `.ogg`), `.m4a`, `.mp3`, `.wav` and video
files such as `.mp4` or `.mkv`. Every input is normalized to 16 kHz mono PCM
with ffmpeg before being handed to Whisper, so WhatsApp exports work out of the
box. Everything runs offline on your machine.

## Requirements

- macOS on Apple Silicon (M-series)
- Python 3.11+
- [ffmpeg](https://ffmpeg.org/) in `PATH` (`brew install ffmpeg`)

## Setup

```bash
cd media-stt
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The Whisper model is downloaded on first run and cached in
`~/.cache/huggingface/hub`, so later runs work without internet.

## Usage

```bash
media-stt "~/Downloads/WhatsApp Audio 2026-10-14 at 10.56.31.opus"   # installed script
python -m media_stt note.opus recording.m4a                          # or as a module

# A whole folder, recursively, forcing Spanish and emitting subtitles
media-stt ~/Downloads/voice-notes -r -l es --srt
```

### Options

| Option | Description |
|---|---|
| `audio` | One or more files, or directories to scan |
| `-o`, `--output` | Output directory (default: `output`) |
| `-m`, `--model` | Whisper MLX model (default: `mlx-community/whisper-medium-mlx`) |
| `-l`, `--language` | Force a language, e.g. `es`, `en` (default: `auto`) |
| `--srt` | Also write a `.srt` subtitle file with timestamps |
| `-r`, `--recursive` | Scan directories recursively |
| `-v`, `--verbose` | Show debug logging |
| `--version` | Print the version and exit |

## Output

For every input `<name>.<ext>` the script writes to the output directory:

- `<name>_<timestamp>.txt` — the plain transcript
- `<name>_<timestamp>.meta` — model, detected language, character count, timing
- `<name>_<timestamp>.srt` — only with `--srt`

## Architecture

One responsibility per module, wired together by a small orchestration layer:

```
src/media_stt/
├── cli.py          # argument parsing and user-facing output
├── config.py       # constants and defaults
├── discovery.py    # expand files/directories into a media file list
├── audio.py        # ffmpeg availability + decode to 16 kHz mono WAV
├── transcriber.py  # Whisper MLX wrapper (Transcription / Segment models)
├── writers.py      # render + persist text, SRT and metadata
├── pipeline.py     # orchestration: decode → transcribe → write
└── utils.py        # time formatting helpers
```

Data flows one way: `cli` → `pipeline` → (`audio`, `transcriber`, `writers`).
`mlx_whisper` is imported lazily, so the package imports and tests run without
MLX installed.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Notes

- First run of a model is slower (download + warm-up).
- A failing file is reported and the batch continues.
- `--model mlx-community/whisper-large-v3-mlx` gives better accuracy at the cost
  of speed and memory.

## License

[MIT](LICENSE) © 2026 kokovrinn
