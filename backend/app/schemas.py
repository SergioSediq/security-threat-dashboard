from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ThreatRecord(BaseModel):
    id: str
    title: str
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    cve_ids: list[str] = Field(default_factory=list)
    mitre_techniques: list[str] = Field(default_factory=list)
    summary: str
    source: str
    observed_at: datetime


class OSINTItem(BaseModel):
    id: str
    title: str
    url: str
    tags: list[str] = Field(default_factory=list)
    fetched_at: datetime


class SituationSummary(BaseModel):
    total_events: int
    critical: int
    mitre_techniques_observed: int
    osint_items: int
