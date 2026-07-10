from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "Alberta Community Intelligence Engine"
    assert response.json()["status"] == "running"


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_entity_links_endpoint() -> None:
    response = client.get("/entity-links")

    assert response.status_code == 200

    links = response.json()

    assert len(links) >= 4
    assert links[0]["match_reasons"]
    assert links[0]["score"] > 0


def test_job_links_endpoint() -> None:
    response = client.get("/job-links")

    assert response.status_code == 200

    links = response.json()

    assert len(links) == 4
    assert links[0]["score"] >= links[-1]["score"]
    assert links[0]["match_reasons"]


def test_job_posting_service_links_endpoint() -> None:
    response = client.get(
        "/job-postings/ziprecruiter-z003/service-links",
    )

    assert response.status_code == 200

    links = response.json()

    assert len(links) == 2
    assert {link["service_id"] for link in links} == {
        "community-A103",
        "informalberta-3",
    }


def test_reddit_post_service_links_endpoint() -> None:
    response = client.get("/social-posts/reddit/reddit-r001/service-links")

    assert response.status_code == 200

    links = response.json()

    assert len(links) == 2
    assert {link["service_id"] for link in links} == {
        "community-A101",
        "informalberta-1",
    }


def test_reddit_post_service_links_endpoint_returns_empty_for_unmatched_post() -> None:
    response = client.get("/social-posts/reddit/reddit-r002/service-links")

    assert response.status_code == 200
    assert response.json() == []


def test_recommendations_endpoint_returns_ranked_results() -> None:
    response = client.get("/recommendations")

    assert response.status_code == 200

    recommendations = response.json()

    assert len(recommendations) == 6
    assert recommendations[0]["rank"] == 1
    assert recommendations[0]["score"] >= recommendations[-1]["score"]
    assert recommendations[0]["service_name"]
    assert recommendations[0]["match_reasons"]


def test_reddit_post_recommendations_endpoint() -> None:
    response = client.get(
        "/social-posts/reddit/reddit-r001/recommendations",
    )

    assert response.status_code == 200

    recommendations = response.json()

    assert len(recommendations) == 2
    assert recommendations[0]["rank"] == 1
    assert recommendations[0]["service_id"] == "community-A101"


def test_cors_allows_local_frontend_origin() -> None:
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:8080"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:8080"
    )


def test_search_endpoint_returns_interpreted_results() -> None:
    response = client.get(
        "/search",
        params={"q": "meal delivery in Stony Plain"},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["interpretation"]["categories"] == ["food_support"]
    assert payload["interpretation"]["locations"] == ["Stony Plain"]
    assert payload["results"]
    assert payload["results"][0]["city"] == "Stony Plain"
    assert payload["answer"]
