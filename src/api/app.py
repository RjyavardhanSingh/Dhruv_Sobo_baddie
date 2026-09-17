"""FastAPI application factory."""

from fastapi import FastAPI

from api.routes import contexts, materials, questions, sessions


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
