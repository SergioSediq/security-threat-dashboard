# Situation — optional deep-dive

This document supplements the main [README.md](./README.md) and [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md). It describes how requests and data move through the stack, where to change behavior, and how tooling fits together.

---

## Why this file exists

The root README is optimized for **getting started** (run commands, endpoint table, Docker ports). This file is for **maintainers**: request flow, module responsibilities, environment semantics, and extension points without repeating every install step.

---

## High-level flow

1. **Browser** loads the SPA (Vite dev on `:5173`, or nginx on `:8080` in Docker).
2. The UI calls relative paths such as `/api/v1/...` (see `frontend/src/api/client.ts`: `base = import.meta.env.VITE_API_BASE ?? ""`).
3. **Development:** Vite proxies `/api`, `/health`, `/docs`, `/openapi.json`, and `/redoc` to `http://127.0.0.1:8000` (`frontend/vite.config.ts`).
4. **Docker Compose:** the `web` service proxies `/api/`, `/health`, `/docs`, and `/openapi.json` to the `api` service at `http://api:8000` (`frontend/nginx.conf`).
5. **FastAPI** (`backend/app/main.py`) mounts versioned routers under `/api/v1`, adds CORS (GET-only for browser origins), runs `RequestIDMiddleware`, and exposes `/health`.

---

## Backend structure (what lives where)

| Area | Role |
|------|------|
| `app/main.py` | App factory, middleware order, router inclusion, `/health`. |
| `app/config.py` | `Settings` via pydantic-settings: `USE_MOCK_DATA`, `CORS_ORIGINS`, `NVD_API_KEY` (optional; not used by repository code in this repo). |
| `app/api/deps.py` | Cached singletons for `SituationRepository` and `SituationService`. |
| `app/api/v1/situation.py` | Summary, OSINT list, MITRE reference map. |
| `app/api/v1/threats.py` | Paginated threats, NDJSON export. |
| `app/api/v1/system.py` | `/meta`, `/version`. |
| `app/services/situation_service.py` | Filtering, pagination, and `threats_all()` for export. |
| `app/repository.py` | **Read model** — returns fixture lists when `use_mock_data` is true; otherwise empty lists. |
| `app/data/fixtures.py` | In-memory `THREATS`, `OSINT_FEED`, `MITRE_LABELS`. |
| `app/schemas.py` | Pydantic models shared by API responses. |
| `app/middleware/request_id.py` | Propagates or generates `x-request-id` on every response. |
| `app/core/version.py` | `__version__` consumed by `/api/v1/version`, `/api/v1/meta`, and `python -m app version`. |
| `app/cli.py` | `python -m app version` / `python -m app config` (prints non-secret settings). |

---

## `USE_MOCK_DATA` semantics

`SituationRepository` checks `get_settings().use_mock_data`:

- **`true` (default):** `threats()` and `osint()` return copies of fixture lists; `summary()` is derived from those rows plus OSINT count; `mitre_reference()` always returns the fixture label map (independent of the flag).
- **`false`:** `threats()` and `osint()` return **empty** lists. The summary then reflects zeros/empties until you replace the repository implementation with a real data source.

There is no database or NVD client in the repository layer today — extending behavior means implementing or swapping `SituationRepository` (or adding a new adapter) while keeping the service/router contracts stable.

---

## API surface (concise map)

Authoritative contract: checked-in [backend/docs/openapi.json](./backend/docs/openapi.json). Regenerate after route or schema changes:

```bash
cd backend
python scripts/export_openapi.py
```

Notable behaviors:

- **`GET /api/v1/threats`** — Query params: `severity`, `limit`, `offset` (service enforces paging and optional severity filter).
- **`GET /api/v1/export/threats.jsonl`** — Streams NDJSON (`application/x-ndjson`) via `SituationService.threats_all()`.
- **`GET /api/v1/mitre/reference`** — JSON object of technique id → label from fixtures.

---

## Frontend structure

| Area | Role |
|------|------|
| `src/App.tsx` | Tabs “Stream” vs “OSINT”; wires `useSituation(severity)` and `useOsint()`. |
| `src/hooks/useSituation.ts` | Parallel fetch: `/api/v1/situation/summary` and `/api/v1/threats` with `limit=100`, `offset=0`, optional `severity`. |
| `src/hooks/useOsint.ts` | Fetches `/api/v1/osint`. |
| `src/api/client.ts` | `getJSON` with optional `VITE_API_BASE` prefix. |
| `src/api/types.ts` | TypeScript shapes mirroring API payloads. |

If the API is unreachable, `useSituation` surfaces an error state that mentions local dev (`uvicorn` on `:8000` and Vite proxying `/api`).

---

## Docker Compose

- **`api`:** builds `backend/Dockerfile`, sets `USE_MOCK_DATA=true` and `CORS_ORIGINS` for Vite and dockerized UI origins, healthcheck against `GET /health`.
- **`web`:** builds `frontend/Dockerfile` (multi-stage: `npm ci`, `npm run build`, nginx serves static assets). Depends on `api` being healthy. UI on host port **8080**, API on **8000**.

---

## Tests and quality

- **Tests:** `backend/tests/` with Starlette `TestClient` against `app.main:app` (`conftest.py`). Run with `pytest` after installing `requirements-dev.txt` (see main README).
- **Lint:** Ruff targets `app`, `tests`, and `scripts` (main README).

---

## Related docs

- [README.md](./README.md) — quickstart, ports, endpoint sketch.
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — short layout table.
- [backend/docs/openapi.json](./backend/docs/openapi.json) — frozen OpenAPI snapshot.
