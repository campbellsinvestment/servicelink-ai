from pathlib import Path

from fastapi import FastAPI

from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
)

from backend.app.services.social_importer import (
    import_reddit_posts,
)

app = FastAPI(
    title="ServiceLink AI",
    description=(
        "An independent research-software prototype for normalizing "
        "community-service data and linking it to social-platform posts."
    ),
    version="0.2.0",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "ServiceLink AI",
        "status": "running",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/services")
def get_services() -> list[dict]:
    informalberta_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "informalberta_services.csv"
    )

    community_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "community_services.csv"
    )

    services = [
        *import_informalberta_services(informalberta_path),
        *import_community_services(community_path),
    ]

    return [service.model_dump() for service in services]

@app.get("/social-posts/reddit")
def get_reddit_posts() -> list[dict]:
    reddit_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "reddit_posts.csv"
    )

    posts = import_reddit_posts(reddit_path)

    return [
        post.model_dump(mode="json")
        for post in posts
    ]

@app.get("/social-posts/reddit/summary")
def get_reddit_summary() -> dict[str, object]:
    reddit_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "reddit_posts.csv"
    )

    posts = import_reddit_posts(reddit_path)

    communities = sorted(
        {
            post.community
            for post in posts
            if post.community
        }
    )

    return {
        "source": "Reddit",
        "total_posts": len(posts),
        "communities": communities,
    }