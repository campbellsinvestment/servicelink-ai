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
Entity Linking
     │
Recommendations + Search
     │
REST API
     │
Dashboard / Graph UI
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
- job posting enrichment
- organization name extraction
- deterministic entity linking between posts and services
- deterministic entity linking between jobs and services
- explainable recommendation scoring
- conversational search over community services
- TF-IDF semantic similarity scoring

## API Layer

FastAPI exposes normalized data for downstream consumers, including
services, social posts, job postings, entity links, job links,
recommendations, and conversational search.

## Presentation Layer

The frontend dashboard includes:

- Overview stats and best match
- Conversational search
- Ranked recommendations
- D3 knowledge graph (posts, jobs, services, organizations)

Delivery options:

- Local Webpack dev server against the API
- Docker Compose (`web` + `api`, nginx proxies `/api`)
- GitHub Pages demo with bundled snapshot data

## Future work

- embedding-based semantic search
- LLM-assisted entity resolution and conversational agents
- geographic proximity scoring
