"""Learning goal domain models."""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class GoalLevel(str, Enum):
    """Rough difficulty the learner is aiming at."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningGoal(BaseModel):
    """What the learner wants to achieve from this practice."""

    model_config = ConfigDict(str_strip_whitespace=True)

    subject: str
    target: str
    level: GoalLevel = GoalLevel.INTERMEDIATE
    deadline: date | None = None
    language: str = "en"
    notes: str | None = None

    @field_validator("subject", "target")
    @classmethod
    def _require_text(cls, value: str) -> str:
        if not value:
            raise ValueError("must not be empty")
        return value
