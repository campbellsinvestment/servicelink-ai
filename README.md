![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-Educational-lightgrey)
![GitHub Pages](https://img.shields.io/badge/demo-GitHub%20Pages-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

# Alberta Community Intelligence Engine (ACIE)

**Live demo:** [campbellsinvestment.github.io/servicelink-ai](https://campbellsinvestment.github.io/servicelink-ai/)  
**Repository:** [github.com/campbellsinvestment/servicelink-ai](https://github.com/campbellsinvestment/servicelink-ai)

The Alberta Community Intelligence Engine is an independent research software prototype exploring how heterogeneous community-service records and social-platform data can be standardized, analyzed, and linked through modern software engineering and AI techniques.

The project demonstrates practical approaches to data normalization, multi-source ingestion, lexical analysis, REST API design, entity linking, explainable recommendations, knowledge-graph visualization, and conversational search using publicly available technologies. It was inspired by publicly described research challenges associated with the University of Alberta's SoDa-TaP project.

This repository is an independent educational and research prototype. It is **not affiliated with** the University of Alberta, SoDa-TaP, AVOID, InformAlberta, or the Bridging Divides program, and does **not** contain any private source code, datasets, or intellectual property.

---

# Quick Start

## Option A — Docker (recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
git clone https://github.com/campbellsinvestment/servicelink-ai.git
cd servicelink-ai
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080).

The `web` service serves the dashboard and proxies `/api/*` to FastAPI, so the browser only needs one origin.

```bash
# stop
docker compose down
```

## Option B — Local development

**Terminal 1 — API**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

API: [http://localhost:8000](http://localhost:8000)  
Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

**Terminal 2 — Frontend**

```bash
cd frontend
npm install
npm run dev
```

Dashboard: [http://localhost:8080](http://localhost:8080)

## Tests

```bash
source .venv/bin/activate
python -m pytest
```

## Public demo (GitHub Pages)

The live site is rebuilt on every push to `main`. It uses a bundled demo-data snapshot (no hosted API required).

Details: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

# Project Vision

Many organizations maintain valuable community information across disconnected systems with inconsistent data structures. At the same time, people express real needs through online platforms such as Reddit and employment websites.

ACIE explores how software can:

- normalize inconsistent datasets
- classify and enrich text using lexical analysis
- connect people with relevant services
- expose standardized data through modern APIs
- support conversational search and explainable recommendations

---

# Current Features

## Data Ingestion

- Import community-service records from multiple CSV schemas
- Import Reddit discussion datasets
- Import Indeed job postings
- Import ZipRecruiter job postings
- Reusable object-oriented adapter architecture for new data sources

## Data Normalization

- Shared Pydantic models
- Alberta geography normalization
- Phone number normalization
- Category normalization
- Timestamp normalization
- Canonical job and service schemas

## Lexical Analysis

- Configurable dictionary-based classification
- Rule-based keyword extraction
- Service category identification
- Social post enrichment during import
- Job posting enrichment during import
- Organization name extraction from service registry

## Entity Linking

- Deterministic social-post-to-service linking
- Deterministic job-posting-to-service linking
- Explainable match reasons and scores
- Category and geography alignment rules
- Keyword overlap and source-trust scoring
- Organization mention scoring

## Recommendations

- Ranked service recommendations API
- Post and service context in each result
- Per-post and global recommendation views

## Conversational Search

- Natural-language service questions via `GET /search?q=...`
- Lexical intent extraction for category and city
- TF-IDF semantic similarity scoring
- Ranked, explainable answers in the dashboard Search tab

## Knowledge Graph

- Columnar D3 visualization: posts → jobs → services → organizations
- Scored match links plus provider and mention relationships
- Hover highlighting and detail panel

## Dashboard

- Overview stats and best-match highlight
- Search, Recommendations, and Graph pages
- Alberta design-token styling

## REST API

- FastAPI with OpenAPI docs at `/docs`
- Services, Reddit posts, job postings, summaries
- Entity links, job links, recommendations
- Conversational search

## Software Engineering

- Object-oriented architecture
- Automated unit and API integration tests
- GitHub Actions CI
- Docker Compose local stack
- GitHub Pages demo deployment
- Modular service layer and type-safe Pydantic models

---

# Current Architecture

```
                CSV Sources
                     │
     ┌───────────────┼───────────────┐
     │               │               │
InformAlberta    Reddit        Job Boards
Community Data                 (Indeed / ZipRecruiter)
     │               │               │
     └───────────────┼───────────────┘
                     │
            CSV Adapter Layer
                     │
             Data Validation
                     │
          Data Normalization
                     │
         Geography Alignment
                     │
          Lexical Analysis
                     │
          Entity Enrichment
                     │
       Deterministic Entity Linking
                     │
   Recommendation Scoring + Search
                     │
              FastAPI REST API
                     │
        Dashboard / Graph / Search UI
              (Webpack + D3)
```

---

# Supported Sources

Current adapters include:

- InformAlberta-style service datasets
- Community-service datasets
- Reddit discussion datasets
- Indeed job postings
- ZipRecruiter job postings

The adapter architecture allows new sources to be added with minimal changes to the ingestion pipeline.

---

# Demonstration Data

All datasets currently included in this repository are fictional demonstration records created for software engineering purposes.

No personal information is collected, scraped, or redistributed.

---

# Technology Stack

### Backend

- Python 3.13
- FastAPI
- Pydantic
- Pandas
- NumPy
- pytest

### Frontend

- JavaScript
- Webpack
- D3.js
- Government of Alberta Design System (`@abgov/design-tokens`)

### Delivery

- Docker Compose
- GitHub Actions (CI + Pages)
- GitHub Pages live demo

### Development

- Git / GitHub
- VS Code / Cursor
- GitHub Copilot

---

# Documentation

- [Development guide](docs/DEVELOPMENT.md) — local run, Docker, Pages, testing
- [Architecture](docs/ARCHITECTURE.md) — system layers
- [API reference](docs/API.md) — endpoint summary
- [Contributing](CONTRIBUTING.md) — setup and PR expectations
- [Frontend](frontend/README.md) — dashboard pages and build

---

# Roadmap

### Completed

- Multi-source CSV ingestion and shared models
- Adapter architecture and REST API
- Geography / lexical analysis / organization extraction
- Deterministic entity linking (posts and jobs)
- Explainable recommendation scoring
- Automated testing and GitHub Actions CI
- Webpack dashboard (Dashboard, Search, Recommendations, Graph)
- D3 knowledge graph
- Conversational search with TF-IDF semantic scoring
- Docker Compose local stack
- GitHub Pages demo deployment

### Planned

- LLM-assisted entity resolution
- Embedding-based semantic search
- Geographic proximity scoring

---

# Research Objectives

This project explores practical approaches to:

- heterogeneous data integration
- AI-assisted software engineering
- information retrieval
- lexical analysis
- entity resolution
- community-service discovery
- explainable recommendation systems
- conversational interfaces

---

# License

This repository is intended for educational, research, and demonstration purposes.
