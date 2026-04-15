from fastapi import APIRouter

from app.config import get_settings
from app.core.version import __version__

router = APIRouter(prefix="/api/v1", tags=["system"])


@router.get("/meta")
def meta() -> dict[str, bool | str]:
    s = get_settings()
    return {"fixture_mode": s.use_mock_data, "version": __version__}


@router.get("/version")
def version() -> dict[str, str]:
    return {"app": "situation-api", "version": __version__}
