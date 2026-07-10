# Development

## Running

```bash
uvicorn backend.app.main:app --reload
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