# Contributing

Thank you for your interest in contributing to the **Alberta Community Intelligence Engine (ACIE)**.

ACIE is an independent research software prototype inspired by publicly described challenges in community-service data integration, social-platform analysis, and explainable AI. It is not affiliated with the University of Alberta, SoDa-TaP, AVOID, InformAlberta, or Bridging Divides.

## Development Setup

```bash
git clone https://github.com/campbellsinvestment/servicelink-ai.git
cd servicelink-ai

python -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt
```

Run the application:

```bash
uvicorn backend.app.main:app --reload
```

Run the tests:

```bash
python -m pytest
```

Run only API integration tests:

```bash
python -m pytest backend/tests/test_api_integration.py
```

## Coding Standards

- Follow PEP 8
- Prefer type hints
- Keep functions focused and testable
- Add unit tests for all new functionality
- Add integration tests when changing API or pipeline behavior
- Maintain backwards compatibility where practical
- Prefer deterministic rules before LLM-based approaches
- Keep recommendation and linking logic explainable

## Pull Requests

Please ensure:

- All tests pass locally (`python -m pytest`)
- GitHub Actions CI passes
- New features include documentation updates in `README.md` and `docs/`
- Code is formatted consistently
- Public APIs remain stable unless the change is intentional

## Commit Style

Use small, focused commits with clear messages. Each feature should ideally include:

- implementation
- tests
- documentation
- expected test output verified locally

Example:

```text
Add explainable recommendation scoring module

Scores service matches using category, geography, keyword overlap, and
trusted source weighting with auditable match reasons.
```

## Project Layout

```text
backend/
    app/
        importers/
        models/
        services/
    tests/
datasets/
docs/
```

See `docs/DEVELOPMENT.md` and `docs/ARCHITECTURE.md` for more detail.
