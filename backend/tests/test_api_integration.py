"""Integration tests for the full HTTP API pipeline."""

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_services_pipeline_returns_normalized_records() -> None:
    response = client.get("/services")

    assert response.status_code == 200

    services = response.json()

    assert len(services) == 6

    categories = {service["category"] for service in services}

    assert categories == {"transportation", "food_support", "home_care"}

    edmonton_service = next(
        service
        for service in services
        if service["service_id"] == "informalberta-1"
    )

    assert edmonton_service["geography"]["city"] == "Edmonton"
    assert edmonton_service["phone"] == "780-555-0101"


def test_reddit_posts_pipeline_returns_enriched_records() -> None:
    response = client.get("/social-posts/reddit")

    assert response.status_code == 200

    posts = response.json()

    assert len(posts) == 4

    transportation_post = next(
        post for post in posts if post["source_record_id"] == "r001"
    )

    assert transportation_post["service_categories"] == ["transportation"]
    assert transportation_post["locations"] == ["Edmonton"]
    assert "transportation" in transportation_post["keywords"]


def test_reddit_summary_reflects_imported_dataset() -> None:
    response = client.get("/social-posts/reddit/summary")

    assert response.status_code == 200

    summary = response.json()

    assert summary == {
        "source": "Reddit",
        "total_posts": 4,
        "communities": ["Alberta", "Edmonton", "alberta"],
    }


def test_job_postings_pipeline_returns_normalized_records() -> None:
    response = client.get("/job-postings")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) == 6

    sources = {job["source"] for job in jobs}

    assert sources == {"Indeed", "ZipRecruiter"}


def test_job_posting_summary_reflects_imported_dataset() -> None:
    response = client.get("/job-postings/summary")

    assert response.status_code == 200

    summary = response.json()

    assert summary["total_jobs"] == 6
    assert summary["sources"] == ["Indeed", "ZipRecruiter"]
    assert "Edmonton, AB" in summary["locations"]
    assert "Stony Plain, AB" in summary["locations"]


def test_entity_links_pipeline_connects_posts_to_services() -> None:
    response = client.get("/entity-links")

    assert response.status_code == 200

    links = response.json()

    assert len(links) == 4

    linked_post_ids = {link["post_id"] for link in links}

    assert linked_post_ids == {"reddit-r001", "reddit-r004"}


def test_entity_links_are_consistent_with_enriched_reddit_posts() -> None:
    posts_response = client.get("/social-posts/reddit")
    links_response = client.get("/entity-links")

    posts = {
        post["post_id"]: post
        for post in posts_response.json()
    }
    links = links_response.json()

    for link in links:
        post = posts[link["post_id"]]
        category_reason = next(
            reason
            for reason in link["match_reasons"]
            if reason.startswith("category:")
        )

        matched_category = category_reason.removeprefix("category:")

        assert matched_category in post["service_categories"]


def test_post_service_links_match_aggregate_entity_links() -> None:
    aggregate_response = client.get("/entity-links")
    post_response = client.get(
        "/social-posts/reddit/reddit-r001/service-links",
    )

    aggregate_links = [
        link
        for link in aggregate_response.json()
        if link["post_id"] == "reddit-r001"
    ]

    assert post_response.json() == aggregate_links
