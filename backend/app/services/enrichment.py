"""Deterministic enrichment for normalized social posts."""

from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.lexical import (
    extract_keywords,
    extract_locations,
    extract_service_categories,
)
from backend.app.services.organizations import extract_organizations


def _build_analysis_text(post: NormalizedSocialPost) -> str:
    parts = [
        value
        for value in (post.body, post.community)
        if value
    ]

    return " ".join(parts)


def enrich_social_post(
    post: NormalizedSocialPost,
    organization_registry: list[str] | None = None,
) -> NormalizedSocialPost:
    """Populate lexical enrichment fields on a social post."""

    analysis_text = _build_analysis_text(post)

    update = {
        "locations": extract_locations(analysis_text),
        "service_categories": extract_service_categories(analysis_text),
        "keywords": extract_keywords(analysis_text),
    }

    if organization_registry is not None:
        update["organizations"] = extract_organizations(
            analysis_text,
            organization_registry,
        )

    return post.model_copy(update=update)
