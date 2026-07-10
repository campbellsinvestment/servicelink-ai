"""Export API responses as static demo data for GitHub Pages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from backend.app.main import app

OUTPUT_PATH = ROOT / "frontend" / "src" / "demo" / "demo.json"

ENDPOINTS = {
    "/services": "/services",
    "/social-posts/reddit/summary": "/social-posts/reddit/summary",
    "/recommendations": "/recommendations",
    "/social-posts/reddit": "/social-posts/reddit",
    "/entity-links": "/entity-links",
    "/job-postings": "/job-postings",
    "/job-links": "/job-links",
}


def main() -> None:
    client = TestClient(app)
    endpoints: dict[str, object] = {}

    for key, path in ENDPOINTS.items():
        response = client.get(path)
        response.raise_for_status()
        endpoints[key] = response.json()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps({"endpoints": endpoints}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote demo data to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
