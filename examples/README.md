# Examples — Situation API

Run the API locally (`uvicorn app.main:app --port 8000` from `backend/`), then:

```bash
curl -sS http://127.0.0.1:8000/api/v1/version | jq .
curl -sS "http://127.0.0.1:8000/api/v1/threats?limit=10&offset=0" | jq .
curl -sS -o threats.jsonl http://127.0.0.1:8000/api/v1/export/threats.jsonl
```

Frozen schema: regenerate `backend/docs/openapi.json` with `make openapi-monitor` from the repo root (POSIX) or:

```bash
cd backend && pip install -r requirements.txt && python scripts/export_openapi.py
```
