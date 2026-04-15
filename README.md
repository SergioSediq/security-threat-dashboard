# Situation — analyst dashboard

Author: **Sergio Sediq**

Small full-stack app: a JSON API plus a React UI for reviewing **fixture** threat rows (CVE IDs, severities, MITRE technique IDs) and a short OSINT list. Defaults stay offline so demos do not depend on NVD rate limits.

## Stack

| Layer    | Choice                          |
|----------|----------------------------------|
| API      | Python 3.12, FastAPI, Pydantic v2 |
| UI       | React 18, Vite, TypeScript       |
| Tests    | pytest, Starlette `TestClient`   |

## Layout

```
backend/
  app/
    api/v1/               # situation, threats, system routers
    core/                 # version string (API + CLI)
    middleware/           # request id
    services/             # pagination / export orchestration
    data/fixtures.py
    repository.py
    schemas.py
    cli.py                # python -m app …
  tests/
docs/
  ARCHITECTURE.md
frontend/
  src/
    api/
    components/
    hooks/
```

## Run locally

Optional API settings: copy **`backend/.env.example`** to **`backend/.env`** (see `app/config.py`).

**API**

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**CLI (optional)**

```bash
cd backend
python -m app version
python -m app config
```

**UI** (Vite dev server proxies `/api`, `/health`, `/docs`, `/openapi.json`, `/redoc` → 8000)

```bash
cd frontend
npm install
npm run dev
```

**Tests**

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

Lint (optional): `pip install -r requirements-dev.txt` then `ruff check app tests scripts`.

Frozen HTTP contract: `docs/openapi.json` (regenerate with `python scripts/export_openapi.py` from `backend/`).

Use a **dedicated** virtualenv in `backend/` (`python -m venv .venv`) and install only this file so global site-packages do not inject unrelated pytest plugins.

## Docker

```bash
docker compose up --build
```

UI on port **8080**, API on **8000**. Set `VITE_API_BASE` only if you serve the SPA from a different origin than the proxy setup expects.

## API (sketch)

| GET | Purpose |
|-----|---------|
| `/api/v1/situation/summary` | Aggregate counts |
| `/api/v1/threats` | Paginated rows (`severity`, `limit`, `offset`) |
| `/api/v1/export/threats.jsonl` | Fixture export (NDJSON) |
| `/api/v1/osint` | OSINT rows |
| `/api/v1/mitre/reference` | Technique id → label |
| `/api/v1/meta` | Fixture flag + version |
| `/api/v1/version` | `{app, version}` |

Responses include an `x-request-id` header from middleware. `USE_MOCK_DATA=false` empties lists until you wire a real repository.

## License

MIT — see [LICENSE](./LICENSE).
