from pathlib import Path

from fastapi import FastAPI

from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
)

from backend.app.services.social_importer import (
    import_reddit_posts,
)

from backend.app.services.job_importer import (
    import_indeed_jobs,
    import_ziprecruiter_jobs,
)

from backend.app.services.entity_linking import build_service_links

from backend.app.services.recommendations import (
    build_post_recommendations,
    build_recommendations,
)

app = FastAPI(
    title="Alberta Community Intelligence Engine",
    description=(
        "An independent research-software prototype for normalizing "
        "community-service data, enriching it with lexical analysis, "
        "and linking it to social-platform posts."
    ),
    version="0.2.0",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "Alberta Community Intelligence Engine",
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

@app.get("/job-postings")
def get_job_postings() -> list[dict]:
    indeed_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "indeed_jobs.csv"
    )

    ziprecruiter_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "ziprecruiter_jobs.csv"
    )

    jobs = [
        *import_indeed_jobs(indeed_path),
        *import_ziprecruiter_jobs(ziprecruiter_path),
    ]

    return [
        job.model_dump(mode="json")
        for job in jobs
    ]


@app.get("/job-postings/summary")
def get_job_posting_summary() -> dict[str, object]:
    indeed_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "indeed_jobs.csv"
    )

    ziprecruiter_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "ziprecruiter_jobs.csv"
    )

    jobs = [
        *import_indeed_jobs(indeed_path),
        *import_ziprecruiter_jobs(ziprecruiter_path),
    ]

    sources = sorted(
        {
            job.source
            for job in jobs
        }
    )

    locations = sorted(
        {
            job.location
            for job in jobs
            if job.location
        }
    )

    return {
        "total_jobs": len(jobs),
        "sources": sources,
        "locations": locations,
    }


@app.get("/entity-links")
def get_entity_links() -> list[dict]:
    links = build_service_links(PROJECT_ROOT)

    return [link.model_dump() for link in links]


@app.get("/social-posts/reddit/{post_id}/service-links")
def get_reddit_post_service_links(post_id: str) -> list[dict]:
    links = build_service_links(PROJECT_ROOT)

    filtered_links = [
        link
        for link in links
        if link.post_id == post_id
    ]

    return [link.model_dump() for link in filtered_links]


@app.get("/recommendations")
def get_recommendations() -> list[dict]:
    recommendations = build_recommendations(PROJECT_ROOT)

    return [
        recommendation.model_dump()
        for recommendation in recommendations
    ]


@app.get("/social-posts/reddit/{post_id}/recommendations")
def get_reddit_post_recommendations(
    post_id: str,
    limit: int = 5,
) -> list[dict]:
    recommendations = build_post_recommendations(
        PROJECT_ROOT,
        post_id,
        limit=limit,
    )

    return [
        recommendation.model_dump()
        for recommendation in recommendations
    ]