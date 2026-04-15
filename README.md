<div align="center">

# Situation

**Analyst dashboard** · JSON API and React UI for fixture threat data (CVEs, severities, MITRE technique IDs) and a short OSINT feed. Runs offline by default so demos do not rely on NVD rate limits or API keys.

[Sergio Sediq](https://github.com/SergioSediq) · [LinkedIn](https://www.linkedin.com/in/sedyagho) · [sediqsergio@gmail.com](mailto:sediqsergio@gmail.com)

[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)

[Architecture](./docs/ARCHITECTURE.md) · [OpenAPI (JSON)](./backend/docs/openapi.json) · [Deep dive](./README.optional.md)

</div>

## Features

| Area | Description |
|------|-------------|
| Summary | Aggregate counts for the current picture |
| Threats | Paginated fixture rows with optional `severity` filter |
| Export | `GET /api/v1/export/threats.jsonl` (NDJSON) |
| MITRE | Technique IDs to labels via `/api/v1/mitre/reference` |
| OSINT | Curated list alongside the main view |
| Tracing | `x-request-id` on responses (middleware) |
| CLI | `python -m app version` and `python -m app config` |
| Contract | Frozen schema at `backend/docs/openapi.json` (regenerate after API changes) |

## Stack

| Layer | Technology |
|-------|------------|
| API | Python 3.12, FastAPI, Pydantic v2, Uvicorn |
| UI | React 18, Vite, TypeScript |
| Tests | pytest, Starlette `TestClient` |
| Lint | Ruff (`requirements-dev.txt`) |

## Repository layout

```
backend/
  app/
    api/v1/               # situation, threats, system
    core/                 # version (API + CLI)
    middleware/           # request id
    services/             # pagination, export
    data/fixtures.py
    repository.py         # read model; replace for live data
    schemas.py
    cli.py
  tests/
  docs/openapi.json
  scripts/export_openapi.py
docs/
  ARCHITECTURE.md
frontend/
  src/
    api/
    components/
    hooks/
```

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for a concise layer overview.

## Local development

**Environment (optional).** Copy [`backend/.env.example`](./backend/.env.example) to `backend/.env` to override CORS, `USE_MOCK_DATA`, or placeholders. See `app/config.py`.

### API (port 8000)

```bash
cd backend
python -m venv .venv
```

Activate: Windows `.venv\Scripts\activate` · macOS/Linux `source .venv/bin/activate`

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- Interactive docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### CLI

```bash
cd backend
python -m app version
python -m app config
```

### Frontend (Vite)

The dev server proxies `/api`, `/health`, `/docs`, `/openapi.json`, and `/redoc` to `http://127.0.0.1:8000`.

```bash
cd frontend
npm ci
npm run dev
```

Use `npm ci` for reproducible installs when a lockfile is present; `npm install` is fine for quick checks.

### Tests and OpenAPI

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

Lint (optional):

```bash
cd backend
ruff check app tests scripts
```

After changing routes or schemas:

```bash
cd backend
python scripts/export_openapi.py
```

Use a dedicated virtualenv under `backend/` so global pytest plugins do not affect this project.

## Docker

```bash
docker compose up --build
```

| Port | Service |
|------|---------|
| 8080 | Web UI (nginx, static SPA; `/api` proxied to the API) |
| 8000 | API |

Set `VITE_API_BASE` only if the SPA is served from an origin that does not match the compose/nginx proxy setup.

## HTTP API (summary)

| Method / path | Purpose |
|---------------|---------|
| `GET /health` | Liveness |
| `GET /api/v1/situation/summary` | Aggregate counts |
| `GET /api/v1/threats` | Paginated rows (`severity`, `limit`, `offset`) |
| `GET /api/v1/export/threats.jsonl` | NDJSON export |
| `GET /api/v1/osint` | OSINT rows |
| `GET /api/v1/mitre/reference` | Technique id to label map |
| `GET /api/v1/meta` | Fixture flag and version |
| `GET /api/v1/version` | `{ app, version }` |

Responses include `x-request-id`. With `USE_MOCK_DATA=false`, threat and OSINT lists are empty until a real repository implementation is wired.

## License

MIT. See [LICENSE](./LICENSE).
