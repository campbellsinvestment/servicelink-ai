# ServiceLink AI

ServiceLink AI is an independent research-software prototype for exploring
how inconsistent community-service records and social-platform posts can be
cleaned, standardized, connected, searched and visualized.

The project was inspired by publicly described software-engineering challenges
associated with the University of Alberta SoDa-TaP research project.

This repository is independent. It is not affiliated with the University of
Alberta, SoDa-TaP, AVOID, InformAlberta or the Bridging Divides program, and it
does not use their private code or research datasets.

## Initial goals

- Import community-service records from inconsistent CSV schemas
- Normalize records into a shared data model
- Import Reddit and job-posting CSV files
- Extract organizations, locations and service categories
- Link social posts to potentially relevant services
- Provide REST API access to the normalized data
- Build an interactive Bootstrap and D3.js interface
- Add a conversational search experience
- Validate the pipeline with automated tests

## Implemented features

- Shared Pydantic models for normalized records
- Reusable object-oriented CSV adapter architecture
- Community-service ingestion from inconsistent CSV schemas
- Category and phone-number normalization
- Reddit post ingestion and timestamp normalization
- REST API endpoints for services and social posts
- Automated unit and integration tests

## Demonstration data

All social-platform and community-service records currently
included in this repository are fictional demonstration data.

The project does not currently scrape or redistribute real
personal information from social-platform users.

## Technology

- Python
- FastAPI
- Pandas
- NumPy
- JavaScript
- Bootstrap
- D3.js
- Webpack
- pytest