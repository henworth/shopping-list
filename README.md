# shopping-list — Shopping List Service

FastAPI + SQLAlchemy + Postgres CRUD service for the shopping list. Calls `pantry` when an item is marked purchased so it ends up in the pantry. Managed with `uv`.

## Endpoints

All endpoints are served under `${API_PREFIX}` (default `/shopping`). In an ephemeral environment the prefix becomes `/<envName>/shopping`.

| Method | Path | Description |
| --- | --- | --- |
| GET | `/healthz` | Liveness |
| POST | `/list` | Add an item to buy |
| GET | `/list` | List (filter: `purchased=true` or `purchased=false`) |
| GET | `/list/{id}` | Read one |
| PATCH | `/list/{id}` | Partial update |
| DELETE | `/list/{id}` | Delete |
| POST | `/list/{id}/purchase` | Calls `pantry` to create the pantry item, then marks purchased |

## Environment

- `DATABASE_URL` — SQLAlchemy URL for the per-env shopping DB
- `API_PREFIX` — path prefix (default `/shopping`)
- `PANTRY_INTERNAL_URL` — full URL to the `pantry` service endpoint (with prefix). In an ephemeral environment this is `http://pantry:8000/<envName>/pantry` via ECS Service Connect.
- `PANTRY_REQUEST_TIMEOUT_SECONDS` — optional, default 5

## Local dev

Natively with `uv` (just this service; pantry must be reachable at `PANTRY_INTERNAL_URL`):

```bash
uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8001
```

For the full cross-service stack (postgres + pantry + shopping-list with hot reload), check out the [infra repo](https://github.com/your-org/infra) as a sibling of this one and run:

```bash
cd ../infra
docker compose -f docker-compose.dev.yaml up --build
curl http://localhost:8001/shopping/healthz
```
