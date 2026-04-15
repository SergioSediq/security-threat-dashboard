from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    use_mock_data: bool = True
    nvd_api_key: str | None = None
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:8080,http://127.0.0.1:8080"
    )

    @field_validator("cors_origins")
    @classmethod
    def strip_origins(cls, v: str) -> str:
        return v.strip()


@lru_cache
def get_settings() -> Settings:
    return Settings()
