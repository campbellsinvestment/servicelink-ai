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
- organization name extraction
- job posting enrichment and service linking
- deterministic entity linking between posts and services
- explainable recommendation scoring
- conversational search over community services
- TF-IDF semantic similarity scoring

## API Layer

FastAPI exposes normalized data for downstream consumers.

The frontend includes a D3 knowledge graph that visualizes entity links
between Reddit posts, job postings, community services, and organizations.

Future work includes

- embedding-based semantic search
- LLM-assisted conversational agents