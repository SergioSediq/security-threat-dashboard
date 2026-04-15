# Situation — layout

Python layout mirrors larger services: transport (`app/api`), use-cases (`app/services`), adapters (`app/repository` + `app/data/fixtures`), and cross-cutting helpers (`app/core`, `app/middleware`).

| Path | Role |
|------|------|
| `app/api/v1` | Versioned REST routers |
| `app/services` | Filtering, pagination, export orchestration |
| `app/repository` | Read model; swap implementation without changing HTTP |
| `app/middleware` | Request correlation id |
| `app/core` | `__version__` shared by FastAPI `app`, `/api/v1/meta`, and CLI |
| `app/cli.py` | `python -m app` operator commands (`version`, `config`) |

The UI is a Vite SPA; in Docker, nginx proxies `/api` to this service.
