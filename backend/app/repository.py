"""Read path for situation data. Mock store today; same interface can back a DB."""

from app.config import get_settings
from app.data.fixtures import MITRE_LABELS, OSINT_FEED, THREATS
from app.schemas import OSINTItem, SituationSummary, ThreatRecord


class SituationRepository:
    def threats(self) -> list[ThreatRecord]:
        if not get_settings().use_mock_data:
            return []
        return list(THREATS)

    def osint(self) -> list[OSINTItem]:
        if not get_settings().use_mock_data:
            return []
        return list(OSINT_FEED)

    def summary(self) -> SituationSummary:
        rows = self.threats()
        techniques = {t for row in rows for t in row.mitre_techniques}
        return SituationSummary(
            total_events=len(rows),
            critical=sum(1 for r in rows if r.severity == "CRITICAL"),
            mitre_techniques_observed=len(techniques),
            osint_items=len(self.osint()),
        )

    def mitre_reference(self) -> dict[str, str]:
        return dict(MITRE_LABELS)
