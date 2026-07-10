![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-Educational-lightgrey)

# Alberta Community Intelligence Engine (ACIE)

The Alberta Community Intelligence Engine is an independent research software prototype exploring how heterogeneous community-service records and social-platform data can be standardized, analyzed, and linked through modern software engineering and AI techniques.

The project demonstrates practical approaches to data normalization, multi-source ingestion, lexical analysis, REST API design, and entity linking using publicly available technologies. It was inspired by publicly described research challenges associated with the University of Alberta's SoDa-TaP project.

This repository is an independent educational and research prototype. It is **not affiliated with** the University of Alberta, SoDa-TaP, AVOID, InformAlberta, or the Bridging Divides program, and does **not** contain any private source code, datasets, or intellectual property.

---

# Project Vision

Many organizations maintain valuable community information across disconnected systems with inconsistent data structures. At the same time, people express real needs through online platforms such as Reddit and employment websites.

ACIE explores how software can:

- normalize inconsistent datasets
- classify and enrich text using lexical analysis
- connect people with relevant services
- expose standardized data through modern APIs
- provide a foundation for conversational search and AI-assisted decision support

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
- Organization name extraction from service registry
- Employment classification
- Technology skill detection
- Healthcare and senior-support classification

## Entity Linking

- Deterministic social-post-to-service linking
- Explainable match reasons and scores
- Category and geography alignment rules
- Keyword overlap and source-trust scoring
- Organization mention scoring
- REST endpoints for linked recommendations

## Recommendations

- Ranked service recommendations API
- Post and service context in each result
- Per-post and global recommendation views

## Knowledge Graph

- D3 force-directed graph in the frontend
- Posts, services, and organizations as nodes
- Match, provider, and mention relationships from entity links

## REST API

- FastAPI
- OpenAPI documentation
- Aggregated service endpoints
- Reddit endpoints
- Job posting endpoints
- Summary endpoints

## Software Engineering

- Object-oriented architecture
- Automated unit tests
- API integration tests
- GitHub Actions CI
- Modular service layer
- Reusable import pipeline
- Type-safe Pydantic models

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
        Explainable Recommendation Scoring
                     │
              FastAPI REST API
                     │
        Future AI / Search Layer
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

- Python
- FastAPI
- Pandas
- NumPy
- Pydantic

### Frontend

- JavaScript
- Webpack
- Government of Alberta Design System
- Bootstrap-inspired layout tokens
- D3.js

### Development

- pytest
- Git
- GitHub
- VS Code
- Cursor
- GitHub Copilot

---

# Roadmap

### Completed

- Multi-source CSV ingestion
- Shared data models
- Adapter architecture
- REST API
- Geography normalization
- Lexical analysis
- Deterministic entity linking
- Automated testing
- API integration tests
- GitHub Actions CI
- Explainable recommendation scoring
- Organization name extraction
- Webpack dashboard scaffold
- D3.js knowledge graph visualization

### In Progress

- Conversational search

### Planned

- LLM-assisted entity resolution
- Semantic search
- Geographic proximity scoring
- Interactive dashboard

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