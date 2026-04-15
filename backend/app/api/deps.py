from functools import lru_cache

from app.repository import SituationRepository
from app.services.situation_service import SituationService


@lru_cache
def repo() -> SituationRepository:
    return SituationRepository()


@lru_cache
def situation_service() -> SituationService:
    return SituationService(repo())
