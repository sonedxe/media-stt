# Contributing to Media STT

Thanks for considering contributing to Media STT.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development

```bash
ruff check .
ruff format .
pytest
```

## Guidelines

1. Keep modules focused: one responsibility per file under `src/media_stt/`.
2. Add or update tests under `tests/` for any behaviour change.
3. Prefer pure functions where possible so logic stays easy to test.
4. Run `ruff check .` and `pytest` before opening a Pull Request.

## Reporting issues

Open an [issue](https://github.com/kokovrinn/media-stt/issues) describing the
problem, the command you ran, and a sample of any error output.
