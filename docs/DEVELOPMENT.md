# Development

## Quick Start (Docker)

```bash
docker compose up --build
```

Open `http://localhost:8080`.

| Service | Role |
|---------|------|
| `api` | FastAPI on port 8000 (internal) |
| `web` | nginx dashboard; proxies `/api/*` → API |

```bash
docker compose down
```

Requires Docker Desktop. If `docker` is not found, install it first, then open Docker Desktop before running Compose.

## Local Development (without Docker)

Backend API:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

Frontend dashboard:

```bash
cd frontend
npm install
npm run dev
```

| App | URL |
|-----|-----|
| Dashboard | http://localhost:8080 |
| API | http://localhost:8000 |
| OpenAPI docs | http://localhost:8000/docs |

## GitHub Pages

The live demo is published from the `main` branch via GitHub Actions.

**URL:** `https://campbellsinvestment.github.io/servicelink-ai/`

Each push to `main` runs `.github/workflows/pages.yml`, which:

1. Exports a demo API snapshot (`scripts/export_demo_data.py`)
2. Builds the frontend in demo mode with the `/servicelink-ai/` asset path
3. Deploys `frontend/dist` to GitHub Pages

The public site uses bundled demo data so it works without a hosted API.
Local Docker and `npm run dev` talk to the live FastAPI server.

Reproduce the Pages build locally:

```bash
python scripts/export_demo_data.py
cd frontend
ACIE_DEMO_MODE=true WEBPACK_PUBLIC_PATH=/servicelink-ai/ npm run build:pages
```

## Testing

```bash
python -m pytest
```

Run only integration tests:

```bash
python -m pytest backend/tests/test_api_integration.py
```

## Continuous Integration

GitHub Actions runs the full pytest suite on every push and pull request
to `main`. See `.github/workflows/ci.yml`.

## Current Folder Structure

```
backend/
    app/
        importers/
        models/
        services/
    tests/

frontend/
    src/
    Dockerfile
    nginx.conf

datasets/
    raw/
    processed/

docs/
scripts/
    export_demo_data.py

Dockerfile
docker-compose.yml
.github/workflows/
    ci.yml
    pages.yml
```

## Current Pipeline

```
CSV sources
    ↓
Adapters + validation
    ↓
Normalization + geography
    ↓
Lexical enrichment
    ↓
Entity linking (posts / jobs → services)
    ↓
Recommendations + conversational search
    ↓
FastAPI
    ↓
Dashboard (Search, Recommendations, Graph)
```
