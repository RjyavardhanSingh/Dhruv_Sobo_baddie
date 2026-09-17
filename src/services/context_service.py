"""Context building service — builds context and caches in Dragonfly."""

from __future__ import annotations

from cache.dragonfly import CacheService
from context import ContextBuilder
from db.connection import Database
from models import LearningGoal


async def build_and_store_context(
    db: Database,
    cache: CacheService,
    material_ids: list[str],
    goal: LearningGoal,
) -> dict:
    """Build a LearningContext from materials + goal, store in DB and cache.

    Returns the context as a dict.
    """
    builder = ContextBuilder().with_goal(goal)

    for mid in material_ids:
        row = await db.fetchrow("SELECT * FROM materials WHERE id = $1", mid)
        if row is None:
            raise ValueError(f"Material not found: {mid}")

        from ingestion import extract_text
        from models import MaterialKind

        kind = MaterialKind(row["kind"])
        doc = extract_text(row["full_text"], name=row["name"], kind=kind)
        builder.add_source(doc)

    context = builder.build()

    await db.execute(
        """INSERT INTO contexts (id, subject, target, level, deadline, language,
              source_count, page_count, word_count, reading_minutes)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
           ON CONFLICT (id) DO NOTHING""",
        context.context_id,
        context.goal.subject,
        context.goal.target,
        context.goal.level.value,
        context.goal.deadline,
        context.goal.language,
        context.stats.source_count,
        context.stats.page_count,
        context.stats.word_count,
        context.stats.reading_minutes,
    )

    for mid in material_ids:
        await db.execute(
            """INSERT INTO context_materials (context_id, material_id)
               VALUES ($1, $2)
               ON CONFLICT DO NOTHING""",
            context.context_id,
            mid,
        )

    cache.set(
        f"context:{context.context_id}",
        context.model_dump(mode="json"),
        ttl=86400,
    )

    return context.model_dump(mode="json")
