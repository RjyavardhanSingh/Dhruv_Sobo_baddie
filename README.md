# Self Learning Platform

PDF extraction agent for the Self Learning Platform.

## Structure

```
.
├── src/agent/        # Package source (import `agent`)
│   ├── __init__.py   # CLI entry-point `agent`
│   └── pdf.py        # PDF extraction (pymupdf + pydantic)
├── tests/            # pytest suite
├── data/             # Sample PDFs
├── pyproject.toml    # Project metadata & tooling
└── uv.lock           # Locked dependencies
```

## Setup

Requires Python >=3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync              # install main dependencies
uv sync --group dev  # install dev dependencies (pytest, ruff)
```

## Usage

```bash
# CLI entry point
uv run agent

# Extract PDF via Python
uv run python -c "from agent.pdf import extract_pdf; print(extract_pdf('data/test_biology.pdf').full_text[:500])"

# Format / lint
uv run ruff check src tests
uv run ruff format src tests
```

## Testing

```bash
uv run pytest -v
```
