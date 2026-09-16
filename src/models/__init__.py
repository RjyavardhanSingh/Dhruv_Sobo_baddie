"""Shared domain models for the self-learning platform."""

from models.context import ContextStats, LearningContext
from models.goal import GoalLevel, LearningGoal
from models.material import (
    MaterialKind,
    SourceDocument,
    SourcePage,
    build_source_document,
)

__all__ = [
    "ContextStats",
    "GoalLevel",
    "LearningContext",
    "LearningGoal",
    "MaterialKind",
    "SourceDocument",
    "SourcePage",
    "build_source_document",
]
