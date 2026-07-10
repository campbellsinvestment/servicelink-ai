from pathlib import Path

from backend.app.services.recommendations import (
    build_post_recommendations,
    build_recommendations,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_build_recommendations_ranks_by_score() -> None:
    recommendations = build_recommendations(PROJECT_ROOT)

    assert len(recommendations) == 6
    assert recommendations[0].rank == 1
    assert recommendations[0].score >= recommendations[-1].score
    assert recommendations[0].match_reasons


def test_build_recommendations_include_post_and_service_context() -> None:
    recommendations = build_recommendations(PROJECT_ROOT)

    top_recommendation = recommendations[0]

    assert top_recommendation.post_id.startswith("reddit-")
    assert top_recommendation.service_name
    assert top_recommendation.organization
    assert top_recommendation.city
    assert top_recommendation.category


def test_build_post_recommendations_returns_ranked_matches_for_one_post() -> None:
    recommendations = build_post_recommendations(
        PROJECT_ROOT,
        "reddit-r001",
    )

    assert len(recommendations) == 2
    assert recommendations[0].rank == 1
    assert recommendations[0].post_id == "reddit-r001"
    assert recommendations[0].service_id == "community-A101"
    assert "keywords:" in recommendations[0].match_reasons[2]


def test_build_post_recommendations_respects_limit() -> None:
    recommendations = build_post_recommendations(
        PROJECT_ROOT,
        "reddit-r001",
        limit=1,
    )

    assert len(recommendations) == 1
    assert recommendations[0].service_id == "community-A101"
