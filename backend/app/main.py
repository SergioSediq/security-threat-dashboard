from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import situation, system, threats
from app.config import get_settings
from app.core.version import __version__
from app.middleware.request_id import RequestIDMiddleware

settings = get_settings()

app = FastAPI(
    title="Situation API",
    version=__version__,
    description="Feeds an analyst dashboard; fixture-backed by default.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)

app.include_router(situation.router)
app.include_router(threats.router)
app.include_router(system.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
