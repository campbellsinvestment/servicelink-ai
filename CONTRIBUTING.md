# Contributing

Thank you for your interest in contributing to ServiceLink AI.

## Development Setup

```bash
git clone https://github.com/<yourusername>/servicelink-ai
cd servicelink-ai

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Run the application

```bash
uvicorn backend.app.main:app --reload
```

Run the tests

```bash
python -m pytest
```

## Coding Standards

- Follow PEP 8
- Prefer type hints
- Keep functions focused and testable
- Add unit tests for all new functionality
- Maintain backwards compatibility where practical

## Pull Requests

Please ensure:

- All tests pass
- New features include documentation
- Code is formatted consistently
- Public APIs remain stable