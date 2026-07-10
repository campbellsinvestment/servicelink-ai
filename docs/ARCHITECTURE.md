# Architecture

The system is organized into several independent layers.

```
CSV Sources
     │
CSV Adapters
     │
Normalization
     │
Lexical Analysis
     │
Entity Enrichment
     │
REST API
```

## Adapter Layer

Each data source has its own adapter responsible for converting
source-specific schemas into shared Pydantic models.

## Normalization Layer

Responsible for

- category normalization
- phone normalization
- Alberta geography normalization
- timestamp normalization

## Analysis Layer

Responsible for

- lexical classification
- keyword extraction
- service categorization
- social post enrichment
- deterministic entity linking between posts and services

## API Layer

FastAPI exposes normalized data for downstream consumers.

Future work includes

- semantic search
- conversational AI
- recommendation ranking improvements
- knowledge graph generation