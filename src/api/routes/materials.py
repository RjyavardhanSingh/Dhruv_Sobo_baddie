"""Material upload routes."""

from fastapi import APIRouter, Depends, HTTPException

from api.schemas import MaterialResponse, MaterialUpload
from cache import CacheService, get_cache
from db.connection import Database, get_db
from services import material_service

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("", response_model=MaterialResponse)
async def upload_material(
    payload: MaterialUpload,
    db: Database = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    """Upload pasted text or markdown as a material."""
    doc = await material_service.upload_text(
        db, payload.content, name=payload.name, kind=payload.kind
    )
    return MaterialResponse(
        id=doc.source_id,
        name=doc.name,
        kind=doc.kind.value,
        page_count=doc.page_count,
        word_count=doc.word_count,
    )


@router.get("/{material_id}", response_model=MaterialResponse)
async def get_material(
    material_id: str,
    db: Database = Depends(get_db),
):
    """Fetch a material by ID."""
    record = await material_service.get_material(db, material_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return MaterialResponse(
        id=record["id"],
        name=record["name"],
        kind=record["kind"],
        page_count=record["page_count"],
        word_count=record["word_count"],
    )
