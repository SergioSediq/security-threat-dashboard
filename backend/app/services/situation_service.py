from __future__ import annotations

from app.repository import SituationRepository
from app.schemas import ThreatRecord


class SituationService:
    """Use-case layer on top of the repository (fixtures today, storage later)."""

    def __init__(self, repo: SituationRepository) -> None:
        self._repo = repo

    def threats_page(
        self,
        *,
        severity: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[ThreatRecord], int]:
        rows = list(self._repo.threats())
        if severity:
            rows = [r for r in rows if r.severity == severity]
        total = len(rows)
        page = rows[offset : offset + limit]
        return page, total

    def threats_all(self) -> list[ThreatRecord]:
        return list(self._repo.threats())
