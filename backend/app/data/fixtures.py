"""Offline fixtures. Swap the repository implementation to hit NVD or a queue worker later."""

from datetime import UTC, datetime

from app.schemas import OSINTItem, ThreatRecord

THREATS: list[ThreatRecord] = [
    ThreatRecord(
        id="evt-001",
        title="OpenSSL: hypothetical critical advisory (fixture)",
        severity="CRITICAL",
        cve_ids=["CVE-2024-0001"],
        mitre_techniques=["T1190", "T1059.004"],
        summary="Synthetic row for UI and contract tests.",
        source="fixture",
        observed_at=datetime.now(UTC),
    ),
    ThreatRecord(
        id="evt-002",
        title="Outbound DNS pattern (fixture)",
        severity="MEDIUM",
        cve_ids=[],
        mitre_techniques=["T1071.004", "T1568.002"],
        summary="Synthetic narrative for MITRE column layout.",
        source="fixture",
        observed_at=datetime.now(UTC),
    ),
]

OSINT_FEED: list[OSINTItem] = [
    OSINTItem(
        id="osint-001",
        title="CISA KEV catalog (external reference)",
        url="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        tags=["KEV", "policy"],
        fetched_at=datetime.now(UTC),
    ),
]

MITRE_LABELS: dict[str, str] = {
    "T1190": "Exploit Public-Facing Application",
    "T1059.004": "Command and Scripting Interpreter: Unix Shell",
    "T1071.004": "Application Layer Protocol: DNS",
    "T1568.002": "Dynamic Resolution: Domain Generation Algorithms",
}
