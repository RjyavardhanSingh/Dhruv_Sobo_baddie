# Self Learning Platform

Adaptive oral learning platform. **Phase 1 so far: the context builder** — turn
uploaded notes (PDF / text / Markdown) plus a learning goal into one normalized
`LearningContext` that downstream stages (scope, curriculum, examiner) consume.

## Structure

```
.
├── src/                      # Source modules (each owns one job)
│   ├── models/               # Shared domain models (pydantic)
│   │   ├── material.py       # SourcePage, SourceDocument, MaterialKind
│   │   ├── goal.py           # LearningGoal, GoalLevel
│   │   └── context.py        # ContextStats, LearningContext
│   ├── ingestion/            # Raw uploads -> normalized source documents
│   │   ├── registry.py       # Dispatch by file extension
│   │   ├── pdf.py            # PDF extractor (pymupdf)
│   │   ├── text.py           # Plain-text extractor
│   │   └── markdown.py       # Markdown -> per-heading sections
│   ├── context/              # Source documents + goal -> LearningContext
│   │   └── builder.py        # ContextBuilder / build_context
│   └── cli/                  # Thin command-line shell
├── tests/                    # pytest suite
├── data/                     # Sample PDFs
├── pyproject.toml            # Project metadata & tooling
└── uv.lock                   # Locked dependencies
```

`models` defines the vocabulary, `ingestion` knows file formats, `context`
orchestrates, and `cli` is the outer shell.

## Setup

Requires Python >=3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync              # install main dependencies
uv sync --group dev  # install dev dependencies (pytest, ruff)
```

## Usage

```bash
# Build a context from a PDF, a Markdown file, or pasted text
uv run agent build-context data/test_biology.pdf \
  --subject Biology --target "explain photosynthesis" --level beginner

# Or from Python
uv run python -c "
from context import ContextBuilder
from models import LearningGoal
ctx = (ContextBuilder()
       .with_goal(LearningGoal(subject='Biology', target='explain photosynthesis'))
       .add_file('data/test_biology.pdf')
       .add_text('# Extra notes\n\nCells are the unit of life.', name='extra.md')
       .build())
print(ctx.context_id, ctx.stats)
"

# Format / lint
uv run ruff check src tests
uv run ruff format src tests
```

## Testing

```bash
uv run pytest -v
```
