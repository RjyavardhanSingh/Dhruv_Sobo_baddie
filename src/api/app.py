"""FastAPI application factory."""

# from pylogs_hook import patch; patch()

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from api.routes import contexts, materials, questions, sessions

load_dotenv()

SCHEMA_PATH = Path(__file__).parent.parent / "db" / "schema.sql"


# Nishnat bahi aap dekhlena ki database app startup p chle ya
# Alg se chlana hai, mne abhi startup p event add krdiya h
# also object storage bhi ready aap uplaod kr skte m apko
# env creds dedunga kl subh aur mera cred chiye toh vo bhi
# bta dena
@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Starting server, applying schema...")
    from db.connection import get_pool

    pool = await get_pool()
    schema = SCHEMA_PATH.read_text()
    await pool.execute(schema)
    logger.info("Schema applied successfully")
    yield


def create_app() -> FastAPI:
    """Build and configure the FastAPI application — 6-step loop order."""
    app = FastAPI(
        title="Adaptive Oral Learning Platform",
        version="0.1.0",
        lifespan=lifespan,
        openapi_tags=[
            {"name": "Upload", "description": "Step 1 — Add study material"},
            {"name": "Goal", "description": "Step 2 — Define goal → context"},
            {"name": "Preparing", "description": "Step 3 — Generate practice set (LLM-tested)"},
            {"name": "Practice", "description": "Step 4 — Answer one at a time"},
            {"name": "Results", "description": "Step 5 — Readiness + weak areas"},
            {"name": "Retest", "description": "Step 6 — One-tap weak-area retest"},
        ],
    )

    # Order matters for docs: Upload → Goal → Preparing → Practice/Results/Retest
    app.include_router(materials.router)
    app.include_router(contexts.router)
    app.include_router(questions.router)
    app.include_router(sessions.router)

    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
