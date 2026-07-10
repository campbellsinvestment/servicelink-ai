# ACIE Frontend

Webpack dashboard for the Alberta Community Intelligence Engine.

## Stack

- JavaScript
- Webpack
- D3.js (knowledge graph)
- Government of Alberta Design System (`@abgov/design-tokens`)

## Pages

- **Dashboard** — stats and best match
- **Recommendations** — ranked post-to-service matches
- **Graph** — force-directed view of posts, services, and organizations

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

## Docker

From the repository root:

```bash
docker compose up --build
```

Opens the dashboard at `http://localhost:8080` with the API proxied at `/api`.

## Build

```bash
npm run build
```

Production assets are written to `frontend/dist/`.

## GitHub Pages

See [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md#github-pages) for deployment
details. The live site uses bundled demo data exported from the backend.
