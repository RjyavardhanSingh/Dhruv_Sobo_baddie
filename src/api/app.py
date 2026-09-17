"""FastAPI application factory."""

from pylogs_hook import patch; patch()  

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import contexts, materials, questions, sessions

SCHEMA_PATH = Path(__file__).parent.parent / "db" / "schema.sql"

#Nishnat bahi aap dekhlena ki database app startup p chle ya
#Alg se chlana hai, mne abhi startup p event add krdiya h
#also object storage bhi ready aap uplaod kr skte m apko
#env creds dedunga kl subh aur mera cred chiye toh vo bhi
#bta dena
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
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="Adaptive Oral Learning Platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(materials.router)
    app.include_router(contexts.router)
    app.include_router(questions.router)
    app.include_router(sessions.router)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
