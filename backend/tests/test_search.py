from pathlib import Path

from backend.app.services.search import interpret_query, search_services


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_interpret_query_extracts_category_and_city() -> None:
    interpretation = interpret_query(
        "Where can I find transportation for seniors in Edmonton?",
    )

    assert interpretation.categories == ["transportation"]
    assert interpretation.locations == ["Edmonton"]
    assert "transportation" in interpretation.summary.lower()
    assert "Edmonton" in interpretation.summary


def test_search_services_returns_ranked_edmonton_transportation() -> None:
    response = search_services(
        PROJECT_ROOT,
        "I need rides to medical appointments in Edmonton",
    )

    assert response.results
    assert response.results[0].rank == 1
    assert response.results[0].city == "Edmonton"
    assert response.results[0].category == "transportation"
    assert response.results[0].score >= response.results[-1].score
    assert "Senior Transportation" in response.answer or "Transportation" in response.answer


def test_search_services_returns_empty_for_unrelated_query() -> None:
    response = search_services(
        PROJECT_ROOT,
        "Looking for a warehouse job near the airport",
    )

    assert response.results == []
    assert "could not find" in response.answer.lower() or "Try asking" in response.answer
