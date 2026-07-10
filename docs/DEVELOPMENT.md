# Development

## Running

```bash
uvicorn backend.app.main:app --reload
```

## Testing

```bash
python -m pytest
```

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