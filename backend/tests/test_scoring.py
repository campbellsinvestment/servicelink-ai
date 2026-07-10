from backend.app.models.service import NormalizedService
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.scoring import (
    find_keyword_overlap,
    score_service_match,
    source_trust_bonus,
    tokenize,
)


def test_tokenize_removes_stop_words_and_short_tokens() -> None:
    tokens = tokenize("The cats are on the table for my mother")

    assert tokens == {"cats", "mother", "table"}


def test_find_keyword_overlap_counts_shared_service_terms() -> None:
    post = NormalizedSocialPost(
        post_id="reddit-r001",
        source="Reddit",
        source_record_id="r001",
        body=(
            "Transportation help for my mother needs affordable transportation "
            "to medical appointments in Edmonton."
        ),
    )
    service = NormalizedService(
        service_id="community-A101",
        organization="Edmonton Senior Resources",
        service_name="Transportation Help",
        category="transportation",
        city="Edmonton",
        description="Rides for medical visits and essential appointments",
        source="Community Services",
        source_record_id="A101",
    )

    score, shared_keywords = find_keyword_overlap(post, service)

    assert score == 9
    assert shared_keywords == ["appointments", "medical", "transportation"]


def test_source_trust_bonus_prefers_informalberta() -> None:
    informalberta_service = NormalizedService(
        service_id="informalberta-1",
        organization="Edmonton Seniors Centre",
        service_name="Senior Transportation",
        category="transportation",
        city="Edmonton",
        source="InformAlberta",
        source_record_id="1",
    )
    community_service = NormalizedService(
        service_id="community-A101",
        organization="Edmonton Senior Resources",
        service_name="Transportation Help",
        category="transportation",
        city="Edmonton",
        source="Community Services",
        source_record_id="A101",
    )

    informalberta_score, informalberta_reason = source_trust_bonus(
        informalberta_service,
    )
    community_score, community_reason = source_trust_bonus(community_service)

    assert informalberta_score == 5
    assert informalberta_reason == "source:InformAlberta"
    assert community_score == 2
    assert community_reason == "source:Community Services"


def test_score_service_match_builds_explainable_total() -> None:
    post = NormalizedSocialPost(
        post_id="reddit-r001",
        source="Reddit",
        source_record_id="r001",
        body=(
            "Transportation help for my mother needs affordable transportation "
            "to medical appointments in Edmonton."
        ),
        locations=["Edmonton"],
        service_categories=["transportation"],
    )
    service = NormalizedService(
        service_id="community-A101",
        organization="Edmonton Senior Resources",
        service_name="Transportation Help",
        category="transportation",
        city="Edmonton",
        description="Rides for medical visits and essential appointments",
        source="Community Services",
        source_record_id="A101",
    )

    score, match_reasons = score_service_match(
        post,
        service,
        has_location_match=True,
    )

    assert score == 26
    assert match_reasons == [
        "category:transportation",
        "city:Edmonton",
        "keywords:appointments,medical,transportation",
        "source:Community Services",
    ]
