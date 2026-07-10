# Development

## Running

Backend API:

```bash
uvicorn backend.app.main:app --reload
```

Frontend dashboard:

```bash
cd frontend
npm install
npm run dev
```

The API runs on `http://localhost:8000`. The dashboard runs on
`http://localhost:8080`.

## Docker

Run the full stack with Docker Compose:

```bash
docker compose up --build
```

Then open `http://localhost:8080`.

The `web` service serves the dashboard and proxies `/api/*` to the FastAPI
container, so the browser only needs one origin.

Stop with `Ctrl+C`, or run detached:

```bash
docker compose up --build -d
docker compose down
```

## GitHub Pages

The live demo is published from the `main` branch via GitHub Actions.

**URL:** `https://campbellsinvestment.github.io/servicelink-ai/`

Enable it once in the repository settings:

1. **Settings → Pages → Build and deployment**
2. Set **Source** to **GitHub Actions**

Each push to `main` runs `.github/workflows/pages.yml`, which:

1. Exports a demo API snapshot from the backend test client
2. Builds the frontend in demo mode with the correct `/servicelink-ai/` asset path
3. Deploys `frontend/dist` to GitHub Pages

The public site uses bundled demo data so it works without a hosted API.
Local development still talks to the FastAPI server on port 8000.

To reproduce the Pages build locally:

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

datasets/
    raw/
    processed/

docs/

Dockerfile
docker-compose.yml
```

## Current Pipeline

```
CSV

↓

Validation

↓

Normalization

↓

Enrichment

↓

REST API
```