"""Context building: material + goal -> LearningContext."""

from context.builder import ContextBuilder, ContextBuildError, build_context

__all__ = ["ContextBuildError", "ContextBuilder", "build_context"]
