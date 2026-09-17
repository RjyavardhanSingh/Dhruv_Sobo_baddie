"""Question generation service — generates and caches questions in Dragonfly."""

from __future__ import annotations

from cache.dragonfly import CacheService


async def generate_questions(
    cache: CacheService,
    context_id: str,
    context_data: dict,
    count: int = 10,
) -> list[dict]:
    """Generate practice questions from a cached LearningContext.

    Stores questions in Dragonfly only (no DB).
    Returns list of question dicts.
    """
    goal = context_data.get("goal", {})
    subject = goal.get("subject", "general")
    target = goal.get("target", "general understanding")

    questions = []
    for i in range(count):
        questions.append(
            {
                "id": i + 1,
                "text": f"Explain {target} in the context of {subject} (question {i + 1} of {count}).",
                "topic": subject,
                "difficulty": "medium",
            }
        )

    cache.set(f"questions:{context_id}", questions, ttl=86400)
    return questions


async def get_questions(cache: CacheService, context_id: str) -> list[dict] | None:
    """Fetch cached questions for a context. Returns None if not found."""
    return cache.get(f"questions:{context_id}")
