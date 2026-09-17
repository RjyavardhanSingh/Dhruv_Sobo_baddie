"""Material upload routes."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.schemas import MaterialResponse, MaterialUpload
from db.connection import Database, get_db
from services import material_service

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("", response_model=MaterialResponse)
async def upload_text_material(
    payload: MaterialUpload,
    db: Database = Depends(get_db),
):
    """Upload pasted text or markdown."""
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


@router.post("/upload", response_model=MaterialResponse)
async def upload_file_material(
    file: UploadFile = File(...),
    db: Database = Depends(get_db),
):
    """Upload a PDF file. Stored in Neon Object Storage."""
    data = await file.read()
    doc = await material_service.upload_pdf(db, file.filename or "upload.pdf", data)
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


@router.get("/{material_id}/download")
async def download_material(
    material_id: str,
    db: Database = Depends(get_db),
):
    """Get a presigned download URL for a material's file."""
    record = await material_service.get_material(db, material_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Material not found")
    url = material_service.get_download_url(record)
    if url is None:
        raise HTTPException(status_code=404, detail="No file stored for this material")
    return {"url": url}
