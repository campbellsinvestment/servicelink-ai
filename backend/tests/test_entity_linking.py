from pathlib import Path

from backend.app.services.enrichment import enrich_social_post
from backend.app.services.entity_linking import (
    link_post_to_services,
    link_posts_to_services,
)
from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
)
from backend.app.services.social_importer import import_reddit_posts


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_enriched_posts() -> list:
    reddit_path = PROJECT_ROOT / "datasets" / "raw" / "social" / "reddit_posts.csv"
    posts = import_reddit_posts(reddit_path)

    return [enrich_social_post(post) for post in posts]


def _load_services() -> list:
    informalberta_path = (
        PROJECT_ROOT / "datasets" / "raw" / "services" / "informalberta_services.csv"
    )
    community_path = (
        PROJECT_ROOT / "datasets" / "raw" / "services" / "community_services.csv"
    )

    return [
        *import_informalberta_services(informalberta_path),
        *import_community_services(community_path),
    ]


def test_link_transportation_post_to_edmonton_services() -> None:
    posts = _load_enriched_posts()
    services = _load_services()

    transportation_post = next(
        post for post in posts if post.source_record_id == "r001"
    )

    links = link_post_to_services(transportation_post, services)

    assert [link.service_id for link in links] == [
        "community-A101",
        "informalberta-1",
    ]
    assert all(link.score == 15 for link in links)
    assert links[0].match_reasons == [
        "category:transportation",
        "city:Edmonton",
    ]


def test_link_home_care_post_to_spruce_grove_services() -> None:
    posts = _load_enriched_posts()
    services = _load_services()

    home_care_post = next(
        post for post in posts if post.source_record_id == "r004"
    )

    links = link_post_to_services(home_care_post, services)

    assert [link.service_id for link in links] == [
        "community-A103",
        "informalberta-3",
    ]
    assert all("category:home_care" in link.match_reasons for link in links)
    assert all("city:Spruce Grove" in link.match_reasons for link in links)


def test_link_job_search_post_returns_no_service_links() -> None:
    posts = _load_enriched_posts()
    services = _load_services()

    job_post = next(post for post in posts if post.source_record_id == "r002")

    links = link_post_to_services(job_post, services)

    assert links == []


def test_link_posts_to_services_returns_links_for_all_matching_posts() -> None:
    posts = _load_enriched_posts()
    services = _load_services()

    links = link_posts_to_services(posts, services)

    linked_post_ids = {link.post_id for link in links}

    assert "reddit-r001" in linked_post_ids
    assert "reddit-r004" in linked_post_ids
    assert "reddit-r002" not in linked_post_ids
