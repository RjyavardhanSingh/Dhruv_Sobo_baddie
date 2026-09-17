"""Context creation routes."""

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import ContextCreate, ContextResponse, ContextStatsResponse
from cache import CacheService, get_cache
from db.connection import Database, get_db
from models import LearningGoal
from services import context_service

router = APIRouter(prefix="/contexts", tags=["contexts"])


@router.post("", response_model=ContextResponse)
async def create_context(
    payload: ContextCreate,
    db: Database = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    """Build a learning context from materials + goal. Caches in Dragonfly."""
    goal = LearningGoal(
        subject=payload.subject,
        target=payload.target,
        level=payload.level,
        deadline=payload.deadline,
        language=payload.language,
    )
    try:
        ctx = await context_service.build_and_store_context(db, cache, payload.material_ids, goal)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ContextResponse(
        id=ctx["context_id"],
        subject=ctx["goal"]["subject"],
        target=ctx["goal"]["target"],
        stats=ContextStatsResponse(**ctx["stats"]),
    )
