"""Preparing — build practice set from context (LLM-tested placeholder)."""

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import QuestionGenerate, QuestionListResponse, QuestionResponse
from cache import CacheService, get_cache
from services import question_service

router = APIRouter(prefix="/contexts/{context_id}/questions", tags=["Preparing"])


@router.post("", response_model=QuestionListResponse, summary="Preparing — generate questions")
async def generate_questions(
    context_id: str,
    payload: QuestionGenerate,
    cache: CacheService = Depends(get_cache),
):
    """Step 3 — Preparing: generate practice set. Stores in Dragonfly only."""
    context_data = cache.get(f"context:{context_id}")
    if context_data is None:
        raise HTTPException(status_code=404, detail="Context not found in cache")

    questions = await question_service.generate_questions(
        cache, context_id, context_data, count=payload.count
    )
    return QuestionListResponse(questions=[QuestionResponse(**q) for q in questions])


@router.get("", response_model=QuestionListResponse, summary="Preparing — fetch questions")
async def get_questions(
    context_id: str,
    cache: CacheService = Depends(get_cache),
):
    """Step 3 — Preparing: fetch cached questions."""
    questions = await question_service.get_questions(cache, context_id)
    if questions is None:
        raise HTTPException(status_code=404, detail="Questions not found")
    return QuestionListResponse(questions=[QuestionResponse(**q) for q in questions])
