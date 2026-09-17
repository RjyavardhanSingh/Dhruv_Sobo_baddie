"""Session lifecycle routes."""

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import (
    AnswerResponse,
    AnswerSubmit,
    SessionCompleteResponse,
    SessionCreate,
    SessionResponse,
)
from cache import CacheService, get_cache
from db.connection import Database, get_db
from services import question_service, session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse)
async def create_session(
    payload: SessionCreate,
    cache: CacheService = Depends(get_cache),
):
    """Start a new practice session. Reads questions from Dragonfly."""
    questions = await question_service.get_questions(cache, payload.context_id)
    if questions is None:
        raise HTTPException(status_code=404, detail="Generate questions first")

    state = await session_service.create_session(cache, payload.context_id, questions)
    return SessionResponse(
        id=state["id"],
        context_id=state["context_id"],
        question_count=len(state["questions"]),
        current_index=state["current_index"],
        status=state["status"],
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    cache: CacheService = Depends(get_cache),
):
    """Get current session state."""
    state = await session_service.get_session(cache, session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(
        id=state["id"],
        context_id=state["context_id"],
        question_count=len(state["questions"]),
        current_index=state["current_index"],
        status=state["status"],
    )


@router.post("/{session_id}/answer", response_model=AnswerResponse)
async def submit_answer(
    session_id: str,
    payload: AnswerSubmit,
    cache: CacheService = Depends(get_cache),
):
    """Submit an answer for a question."""
    try:
        record = await session_service.submit_answer(
            cache, session_id, payload.question_index, payload.answer_text
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return AnswerResponse(**record)


@router.post("/{session_id}/complete", response_model=SessionCompleteResponse)
async def complete_session(
    session_id: str,
    cache: CacheService = Depends(get_cache),
    db: Database = Depends(get_db),
):
    """Complete session: compute score, write to DB, clear cache."""
    try:
        state = await session_service.complete_session(cache, db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SessionCompleteResponse(
        id=state["id"],
        readiness_score=state["readiness_score"],
        questions=state["questions"],
        answers=state["answers"],
        scores=state["scores"],
        completed_at=state["completed_at"],
    )
