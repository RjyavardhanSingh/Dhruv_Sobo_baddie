"""FastAPI application factory."""

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402

from api.routes import contexts, materials, questions, sessions  # noqa: E402


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title="Adaptive Oral Learning Platform",
        version="0.1.0",
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
