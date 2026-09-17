"""Material upload and retrieval service."""

from __future__ import annotations

from db.connection import Database
from ingestion import extract_path, extract_text
from models import MaterialKind, SourceDocument


async def upload_file(db: Database, path: str) -> SourceDocument:
    """Ingest a file and store in DB. Returns the source document."""
    doc = extract_path(path)
    await db.execute(
        """INSERT INTO materials (id, name, kind, full_text, page_count, word_count)
           VALUES ($1, $2, $3, $4, $5, $6)
           ON CONFLICT (id) DO NOTHING""",
        doc.source_id,
        doc.name,
        doc.kind.value,
        doc.full_text,
        doc.page_count,
        doc.word_count,
    )
    return doc


async def upload_text(
    db: Database,
    content: str,
    name: str = "pasted-notes.txt",
    kind: MaterialKind = MaterialKind.TEXT,
) -> SourceDocument:
    """Ingest pasted text and store in DB. Returns the source document."""
    doc = extract_text(content, name=name, kind=kind)
    await db.execute(
        """INSERT INTO materials (id, name, kind, full_text, page_count, word_count)
           VALUES ($1, $2, $3, $4, $5, $6)
           ON CONFLICT (id) DO NOTHING""",
        doc.source_id,
        doc.name,
        doc.kind.value,
        doc.full_text,
        doc.page_count,
        doc.word_count,
    )
    return doc


async def get_material(db: Database, material_id: str) -> dict | None:
    """Fetch a material record by ID."""
    row = await db.fetchrow("SELECT * FROM materials WHERE id = $1", material_id)
    return dict(row) if row else None
