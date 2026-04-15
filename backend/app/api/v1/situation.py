from fastapi import APIRouter, Depends

from app.api.deps import repo
from app.repository import SituationRepository
from app.schemas import OSINTItem, SituationSummary

router = APIRouter(prefix="/api/v1", tags=["situation"])


@router.get("/situation/summary", response_model=SituationSummary)
def situation_summary(r: SituationRepository = Depends(repo)) -> SituationSummary:
    return r.summary()


@router.get("/osint")
def list_osint(r: SituationRepository = Depends(repo)) -> dict[str, list[OSINTItem]]:
    return {"items": r.osint()}


@router.get("/mitre/reference")
def mitre_reference(r: SituationRepository = Depends(repo)) -> dict[str, str]:
    return r.mitre_reference()
