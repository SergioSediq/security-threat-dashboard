<div align="center">

# 📊 Situation — analyst dashboard

A **small full-stack app**: a JSON API plus a **React** UI for reviewing **fixture** threat rows (**CVE** IDs, severities, **MITRE** technique IDs) and a short **OSINT** list. Defaults stay **offline** so demos never depend on **NVD** rate limits or live keys.

**Author:** [Sergio Sediq](https://github.com/SergioSediq) · [LinkedIn](https://www.linkedin.com/in/sedyagho) · [sediqsergio@gmail.com](mailto:sediqsergio@gmail.com)

[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)

📖 [Architecture](./docs/ARCHITECTURE.md) · 📄 [OpenAPI JSON](./backend/docs/openapi.json)

</div>

---

## ✨ What you get

- 📈 **Situation summary** — Aggregate counts for the current threat picture  
- 🎯 **Threat grid** — Paginated fixture rows with **severity** filters  
- 📤 **NDJSON export** — `GET /api/v1/export/threats.jsonl` for “pipe to a datastore” demos  
- 🗺️ **MITRE** — Technique IDs resolved to labels (`/api/v1/mitre/reference`)  
- 🌐 **OSINT** — Short curated list next to the main table  
- 🪪 **`x-request-id`** — On every JSON response via middleware  
- ⌨️ **CLI** — `python -m app version` and `python -m app config` without opening Swagger  
- 📜 **OpenAPI snapshot** — Checked in at **`backend/docs/openapi.json`** (regenerate after route changes)  

---

## 🧰 Stack

| Layer | Choice |
| ----- | ------ |
| **API** | Python **3.12**, **FastAPI**, **Pydantic v2**, **Uvicorn** |
| **UI** | **React 18**, **Vite**, **TypeScript** |
| **Tests** | **pytest**, Starlette **`TestClient`** |
| **Lint** | **Ruff** (`requirements-dev.txt`) |

---

## 🗂️ Layout

```
backend/
  app/
    api/v1/               # situation, threats, system routers
    core/                 # version string (API + CLI)
    middleware/           # request id
    services/             # pagination / export orchestration
    data/fixtures.py
    repository.py         # read model; swap for live data here
    schemas.py
    cli.py                # python -m app …
  tests/
  docs/openapi.json       # frozen HTTP contract (regenerate from scripts/)
  scripts/export_openapi.py
docs/
  ARCHITECTURE.md
frontend/
  src/
    api/
    components/
    hooks/
```

More detail: **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)**

---

## 🚀 Run locally

### Optional env

Copy **[`backend/.env.example`](./backend/.env.example)** → **`backend/.env`** if you want to override **CORS**, **`USE_MOCK_DATA`**, or placeholders (see **`app/config.py`**).

---

### 🐍 API (port `8000`)

```bash
cd backend
python -m venv .venv
```

Activate the venv:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- **Swagger:** `http://127.0.0.1:8000/docs`  
- **ReDoc:** `http://127.0.0.1:8000/redoc`  

---

### ⌨️ CLI (optional)

```bash
cd backend
python -m app version
python -m app config
```

---

### 💻 UI (Vite dev server)

The dev server proxies **`/api`**, **`/health`**, **`/docs`**, **`/openapi.json`**, and **`/redoc`** → **`http://127.0.0.1:8000`**.

```bash
cd frontend
npm ci
npm run dev
```

*(Use **`npm ci`** when you have a lockfile and want reproducible installs; **`npm install`** is fine for quick tries.)*

---

### 🧪 Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

**Lint (optional)**

```bash
cd backend
pip install -r requirements-dev.txt
ruff check app tests scripts
```

**Refresh OpenAPI** after you change routes or schemas:

```bash
cd backend
python scripts/export_openapi.py
```

> Use a **dedicated** virtualenv in `backend/` so global site-packages does not inject unrelated **pytest** plugins into this project’s runs.

---

## 🐳 Docker

```bash
docker compose up --build
```

| Port | What |
| ---- | ---- |
| **8080** | UI (nginx + built SPA; proxies **`/api`** to the API) |
| **8000** | API |

Set **`VITE_API_BASE`** only if you serve the SPA from a different origin than the compose / nginx proxy expects.

---

## 📡 API (sketch)

| `GET` | Purpose |
| ----- | ------- |
| `/health` | Liveness |
| `/api/v1/situation/summary` | Aggregate counts |
| `/api/v1/threats` | Paginated rows (`severity`, `limit`, `offset`) |
| `/api/v1/export/threats.jsonl` | Fixture export (NDJSON) |
| `/api/v1/osint` | OSINT rows |
| `/api/v1/mitre/reference` | Technique id → label |
| `/api/v1/meta` | Fixture flag + version |
| `/api/v1/version` | `{app, version}` |

Responses include an **`x-request-id`** header from middleware. **`USE_MOCK_DATA=false`** empties lists until you wire a real **repository** implementation.

---

## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)

---

## 📜 License

**MIT** — see [LICENSE](./LICENSE).
