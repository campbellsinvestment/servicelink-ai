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

    assert len(recommendations) == 4
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