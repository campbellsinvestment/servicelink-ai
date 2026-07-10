"""Deterministic entity linking between social posts and services."""

from backend.app.models.entity_link import ServiceLink
from backend.app.models.service import NormalizedService
from backend.app.models.social_post import NormalizedSocialPost


CATEGORY_MATCH_SCORE = 10
LOCATION_MATCH_SCORE = 5
CATEGORY_ONLY_MATCH_SCORE = 5


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

        match_reasons = [f"category:{service.category}"]

        if post.locations:
            if not _city_matches(post, service):
                continue

            match_reasons.append(f"city:{service.city}")
            score = CATEGORY_MATCH_SCORE + LOCATION_MATCH_SCORE
        else:
            score = CATEGORY_ONLY_MATCH_SCORE

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
