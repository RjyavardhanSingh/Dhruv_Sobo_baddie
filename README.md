# Adaptive Oral Learning Platform

Upload what you're studying, say what you need to achieve, practice by speaking your answers out loud, then get a clear report on what you know, what's weak, and what to retest.

## What's Done

- **Material upload** — PDF (stored in Neon Object Storage), text, Markdown
- **Context builder** — combines uploaded material + learning goal into a `LearningContext`
- **Dragonfly cache** — context cached in Dragonfly (Redis-compatible) for fast reads
- **Database** — Neon PostgreSQL with auto-schema on startup (materials, contexts, sessions tables)
- **Object storage** — Neon Object Storage for PDF files (S3-compatible)
- **CI** — GitHub Actions workflow for lint (ruff) and tests (pytest) on PRs
- **API scaffold** — all endpoints wired up, FastAPI app runs

## What's Not Done

- **Question generation** — endpoint exists but no LLM integration (returns hardcoded placeholder questions)
- **Session flow** — endpoints exist (create, answer, complete) but:
  - Scoring is placeholder (answer length, not understanding)
  - No real evaluation logic
  - No weakness analysis
  - No misconception detection
- **LLM integration** — no actual LLM calls anywhere
- **STT (Speech-to-Text)** — answers are typed for now, voice input is Phase 1 goal
- **Weakness report / results screen** — session completes but no analysis
- **Retest flow** — not implemented
- **Frontend** — API only, no UI
- **Gap detection / research** — no source filling from trusted sources
- **Adaptive questioning** — no follow-up or difficulty adjustment
- **Citations** — no source attribution on questions
- **TTS (Text-to-Speech)** — questions are text only

## Structure

```
src/
├── api/                    # FastAPI routes + app factory
│   ├── app.py              # App startup, lifespan (schema init)
│   ├── schemas.py          # Pydantic request/response models
│   └── routes/
│       ├── materials.py    # Upload text or PDF
│       ├── contexts.py     # Build learning context
│       ├── questions.py    # Generate/fetch questions
│       └── sessions.py     # Session lifecycle
├── cache/                  # Dragonfly (Redis) connection + CacheService
│   └── dragonfly.py
├── db/                     # Neon PostgreSQL connection + schema
│   ├── connection.py       # asyncpg pool wrapper
│   └── schema.sql          # Table definitions (auto-applied on startup)
├── services/               # Business logic
│   ├── material_service.py # Upload text/PDF, object storage integration
│   ├── context_service.py  # Build context, cache in Dragonfly
│   ├── question_service.py # Generate questions, cache only
│   ├── session_service.py  # Session lifecycle, DB write on complete
│   └── object_storage.py   # Neon Object Storage (S3-compatible) client
├── models/                 # Pydantic domain models
├── ingestion/              # PDF/text/Markdown parsers
├── context/                # ContextBuilder (material + goal → context)
└── cli/                    # Paused — not building for now
```

## Setup

Requires Python >=3.11 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync              # install main dependencies
uv sync --group dev  # install dev dependencies (pytest, ruff)
```

## Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://...
DRAGONFLY_URL=redis://:password@localhost:6380
DRAGONFLY_PASSWORD=your_password

# Neon Object Storage
AWS_ENDPOINT_URL_S3=https://...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-2
NEON_STORAGE_BUCKET=materials
```

## Running

```bash
# Start Dragonfly
docker compose up -d

# Start server
uv run uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Swagger docs at `http://localhost:8000/docs`.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/materials` | Upload text/markdown (JSON body) |
| `POST` | `/materials/upload` | Upload PDF file (multipart) |
| `GET` | `/materials/{id}` | Fetch material metadata |
| `GET` | `/materials/{id}/download` | Get presigned download URL |
| `POST` | `/contexts` | Build context from materials + goal |
| `POST` | `/contexts/{id}/questions` | Generate practice questions |
| `GET` | `/contexts/{id}/questions` | Fetch cached questions |
| `POST` | `/sessions` | Start a practice session |
| `GET` | `/sessions/{id}` | Get session state |
| `POST` | `/sessions/{id}/answer` | Submit an answer |
| `POST` | `/sessions/{id}/complete` | Complete session, write to DB |
| `GET` | `/health` | Health check |

## Testing

```bash
uv run pytest -v
```

## Linting

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```
