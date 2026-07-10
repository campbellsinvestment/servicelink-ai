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

tests/
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