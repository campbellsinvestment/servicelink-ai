from backend.app.models.service import NormalizedService
from backend.app.services.semantic import (
    semantic_bonus,
    semantic_similarity_scores,
    service_document,
    tokenize_document,
)


def test_tokenize_document_drops_stop_words() -> None:
    tokens = tokenize_document("The cats are on the table for my mother")

    assert "cats" in tokens
    assert "mother" in tokens
    assert "the" not in tokens


def test_semantic_similarity_ranks_related_service_higher() -> None:
    transportation = NormalizedService(
        service_id="community-A101",
        organization="Edmonton Senior Resources",
        service_name="Transportation Help",
        category="transportation",
        city="Edmonton",
        description="Rides for medical visits and essential appointments",
        source="Community Services",
        source_record_id="A101",
    )
    meals = NormalizedService(
        service_id="community-A102",
        organization="West Park Outreach",
        service_name="Meals on Wheels",
        category="food_support",
        city="Stony Plain",
        description="Meal delivery for seniors living independently",
        source="Community Services",
        source_record_id="A102",
    )

    scores = semantic_similarity_scores(
        "need a ride to a medical appointment",
        [transportation, meals],
    )

    assert scores[transportation.service_id] > scores[meals.service_id]


def test_semantic_bonus_formats_explainable_reason() -> None:
    points, reason = semantic_bonus(0.42)

    assert points > 0
    assert reason == "semantic:0.42"


def test_service_document_includes_core_fields() -> None:
    service = NormalizedService(
        service_id="community-A101",
        organization="Edmonton Senior Resources",
        service_name="Transportation Help",
        category="transportation",
        city="Edmonton",
        description="Rides for medical visits",
        source="Community Services",
        source_record_id="A101",
    )

    document = service_document(service)

    assert "Transportation Help" in document
    assert "Edmonton" in document
    assert "medical" in document
