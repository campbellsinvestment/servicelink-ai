from pathlib import Path

from backend.app.services.enrichment import enrich_social_post
from backend.app.services.social_importer import import_reddit_posts


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REDDIT_DATASET = (
    PROJECT_ROOT / "datasets" / "raw" / "social" / "reddit_posts.csv"
)


def test_import_reddit_posts_returns_enriched_records() -> None:
    posts = import_reddit_posts(REDDIT_DATASET)
    transportation_post = next(
        post for post in posts if post.source_record_id == "r001"
    )

    assert transportation_post.service_categories == ["transportation"]
    assert transportation_post.locations == ["Edmonton"]


def test_enrich_social_post_populates_lexical_fields() -> None:
    posts = import_reddit_posts(REDDIT_DATASET)
    transportation_post = next(
        post for post in posts if post.source_record_id == "r001"
    )

    enriched = enrich_social_post(transportation_post)

    assert enriched.service_categories == ["transportation"]
    assert enriched.locations == ["Edmonton"]
    assert "transportation" in enriched.keywords
    assert enriched.organizations == []


def test_enrich_social_post_uses_community_for_location_hints() -> None:
    posts = import_reddit_posts(REDDIT_DATASET)
    meal_post = next(
        post for post in posts if post.source_record_id == "r003"
    )

    enriched = enrich_social_post(meal_post)

    assert enriched.service_categories == ["food_support"]
    assert enriched.locations == ["Edmonton"]


def test_enrich_social_post_leaves_unrelated_posts_without_categories() -> None:
    posts = import_reddit_posts(REDDIT_DATASET)
    job_post = next(
        post for post in posts if post.source_record_id == "r002"
    )

    enriched = enrich_social_post(job_post)

    assert enriched.service_categories == []
    assert enriched.locations == ["Stony Plain", "Spruce Grove"]
