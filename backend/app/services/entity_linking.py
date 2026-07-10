"""Deterministic entity linking between social posts and services."""

from pathlib import Path

from backend.app.models.entity_link import ServiceLink
from backend.app.models.service import NormalizedService
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
)
from backend.app.services.social_importer import import_reddit_posts
from backend.app.services.scoring import score_service_match


def _city_matches(post: NormalizedSocialPost, service: NormalizedService) -> bool:
    return any(
        location.lower() == service.city.lower()
        for location in post.locations
    )


def link_post_to_services(
    post: NormalizedSocialPost,
    services: list[NormalizedService],
) -> list[ServiceLink]:
    """Link a social post to community services using explainable rules."""

    if not post.service_categories:
        return []

    links: list[ServiceLink] = []

    for service in services:
        if service.category not in post.service_categories:
            continue

        if post.locations:
            if not _city_matches(post, service):
                continue

            score, match_reasons = score_service_match(
                post,
                service,
                has_location_match=True,
            )
        else:
            score, match_reasons = score_service_match(
                post,
                service,
                has_location_match=False,
            )

        links.append(
            ServiceLink(
                post_id=post.post_id,
                service_id=service.service_id,
                score=score,
                match_reasons=match_reasons,
            )
        )

    links.sort(
        key=lambda link: (-link.score, link.service_id),
    )

    return links


def link_posts_to_services(
    posts: list[NormalizedSocialPost],
    services: list[NormalizedService],
) -> list[ServiceLink]:
    """Link multiple social posts to community services."""

    links: list[ServiceLink] = []

    for post in posts:
        links.extend(link_post_to_services(post, services))

    return links


def load_community_services(project_root: Path) -> list[NormalizedService]:
    informalberta_path = (
        project_root
        / "datasets"
        / "raw"
        / "services"
        / "informalberta_services.csv"
    )
    community_path = (
        project_root
        / "datasets"
        / "raw"
        / "services"
        / "community_services.csv"
    )

    return [
        *import_informalberta_services(informalberta_path),
        *import_community_services(community_path),
    ]


def load_reddit_posts(project_root: Path) -> list[NormalizedSocialPost]:
    reddit_path = (
        project_root / "datasets" / "raw" / "social" / "reddit_posts.csv"
    )

    return import_reddit_posts(reddit_path)


def build_service_links(project_root: Path) -> list[ServiceLink]:
    posts = load_reddit_posts(project_root)
    services = load_community_services(project_root)

    return link_posts_to_services(posts, services)
