"""Session lifecycle service — manage sessions in Dragonfly, persist on complete."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from cache.dragonfly import CacheService
from db.connection import Database


async def create_session(cache: CacheService, context_id: str, questions: list[dict]) -> dict:
    """Start a new session. Stores state in Dragonfly."""
    session_id = uuid.uuid4().hex[:16]
    state = {
        "id": session_id,
        "context_id": context_id,
        "questions": questions,
        "answers": [],
        "scores": [],
        "current_index": 0,
        "status": "active",
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    cache.set(f"session:{session_id}", state, ttl=86400)
    return state


async def get_session(cache: CacheService, session_id: str) -> dict | None:
    """Get session state from Dragonfly."""
    return cache.get(f"session:{session_id}")


async def submit_answer(
    cache: CacheService,
    session_id: str,
    question_index: int,
    answer_text: str,
) -> dict:
    """Record an answer for a question. Updates session in Dragonfly.

    Returns the answer record with score.
    """
    state = cache.get(f"session:{session_id}")
    if state is None:
        raise ValueError(f"Session not found: {session_id}")

    score = _score_answer(answer_text)
    feedback = "Good" if score >= 70 else "Needs work"

    answer_record = {
        "question_index": question_index,
        "answer_text": answer_text,
        "score": score,
        "feedback": feedback,
    }

    state["answers"].append(answer_record)
    state["scores"].append({"question_index": question_index, "score": score})
    state["current_index"] = question_index + 1

    cache.set(f"session:{session_id}", state, ttl=86400)

    return answer_record


async def complete_session(
    cache: CacheService,
    db: Database,
    session_id: str,
) -> dict:
    """Complete a session: compute final score, write to DB, clear cache.

    Returns the completed session record.
    """
    state = cache.get(f"session:{session_id}")
    if state is None:
        raise ValueError(f"Session not found: {session_id}")

    scores = state.get("scores", [])
    if scores:
        readiness = round(sum(s["score"] for s in scores) / len(scores))
    else:
        readiness = 0

    state["status"] = "completed"
    state["readiness_score"] = readiness
    state["completed_at"] = datetime.now(timezone.utc).isoformat()

    await db.execute(
        """INSERT INTO sessions (id, context_id, questions, answers, scores,
              readiness_score, started_at, completed_at)
           VALUES ($1, $2, $3::jsonb, $4::jsonb, $5::jsonb, $6, $7, $8)""",
        state["id"],
        state["context_id"],
        __import__("json").dumps(state["questions"]),
        __import__("json").dumps(state["answers"]),
        __import__("json").dumps(state["scores"]),
        readiness,
        state["started_at"],
        state["completed_at"],
    )

    cache.delete(f"session:{session_id}")
    cache.delete(f"questions:{state['context_id']}")

    return state


def _score_answer(answer_text: str) -> int:
    """Placeholder scoring — returns a deterministic score based on length."""
    length = len(answer_text.strip())
    if length == 0:
        return 0
    if length < 20:
        return 30
    if length < 50:
        return 50
    if length < 100:
        return 70
    if length < 200:
        return 85
    return 95
