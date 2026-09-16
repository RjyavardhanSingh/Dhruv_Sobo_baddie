"""The built context handed to downstream stages (scope, curriculum, examiner)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from models.goal import LearningGoal
from models.material import SourceDocument


class ContextStats(BaseModel):
    """Cheap, deterministic numbers about the built context."""

    source_count: int
    page_count: int
    word_count: int
    reading_minutes: int


class LearningContext(BaseModel):
    """Everything known before the practice set is generated."""

    context_id: str
    goal: LearningGoal
    sources: list[SourceDocument] = Field(default_factory=list)
    stats: ContextStats
    built_at: datetime
