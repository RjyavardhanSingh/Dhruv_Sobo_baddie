"""Pydantic request/response models for API endpoints."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from models.goal import GoalLevel
from models.material import MaterialKind

# --- Material ---


class MaterialUpload(BaseModel):
    content: str
    name: str = "pasted-notes.txt"
    kind: MaterialKind = MaterialKind.TEXT


class MaterialResponse(BaseModel):
    id: str
    name: str
    kind: str
    page_count: int
    word_count: int


# --- Context ---


class ContextCreate(BaseModel):
    material_ids: list[str]
    subject: str
    target: str
    level: GoalLevel = GoalLevel.INTERMEDIATE
    deadline: date | None = None
    language: str = "en"


class ContextStatsResponse(BaseModel):
    source_count: int
    page_count: int
    word_count: int
    reading_minutes: int


class ContextResponse(BaseModel):
    id: str
    subject: str
    target: str
    stats: ContextStatsResponse


# --- Questions ---


class QuestionGenerate(BaseModel):
    count: int = Field(default=10, ge=1, le=50)


class QuestionResponse(BaseModel):
    id: int
    text: str
    topic: str | None = None
    difficulty: str | None = None


class QuestionListResponse(BaseModel):
    questions: list[QuestionResponse]


# --- Sessions ---


class SessionCreate(BaseModel):
    context_id: str


class SessionResponse(BaseModel):
    id: str
    context_id: str
    question_count: int
    current_index: int
    status: str


class AnswerSubmit(BaseModel):
    question_index: int
    answer_text: str


class AnswerResponse(BaseModel):
    question_index: int
    score: int
    feedback: str


class SessionCompleteResponse(BaseModel):
    id: str
    readiness_score: int
    questions: list[dict]
    answers: list[dict]
    scores: list[dict]
    completed_at: str
