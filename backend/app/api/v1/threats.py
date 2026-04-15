from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from app.api.deps import situation_service
from app.services.situation_service import SituationService

router = APIRouter(prefix="/api/v1", tags=["threats"])


@router.get("/threats")
def list_threats(
    severity: str | None = Query(None, description="CRITICAL, HIGH, MEDIUM, LOW, or INFO"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    svc: SituationService = Depends(situation_service),
) -> dict:
    items, total = svc.threats_page(severity=severity, limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/export/threats.jsonl")
def export_threats_jsonl(svc: SituationService = Depends(situation_service)) -> StreamingResponse:
    rows = svc.threats_all()

    def gen():
        for r in rows:
            yield (r.model_dump_json() + "\n").encode("utf-8")

    headers = {"Content-Disposition": 'attachment; filename="threats.jsonl"'}
    return StreamingResponse(gen(), media_type="application/x-ndjson", headers=headers)
