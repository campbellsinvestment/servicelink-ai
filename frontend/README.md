# ACIE Frontend

Webpack dashboard for the Alberta Community Intelligence Engine.

## Stack

- JavaScript
- Webpack
- Government of Alberta Design System (`@abgov/web-components`, `@abgov/design-tokens`)

## Development

Start the API first:

```bash
uvicorn backend.app.main:app --reload
```

Install and run the frontend:

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at `http://localhost:8080` and reads data from `http://localhost:8000`.

## Build

```bash
npm run build
```

Production assets are written to `frontend/dist/`.
