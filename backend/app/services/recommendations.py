"""Build ranked, explainable service recommendations."""

from pathlib import Path

from backend.app.models.recommendation import ServiceRecommendation
from backend.app.models.service import NormalizedService
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.entity_linking import (
    build_service_links,
    load_community_services,
    load_reddit_posts,
)


def _build_recommendation(
    rank: int,
    post: NormalizedSocialPost,
    service: NormalizedService,
    *,
    score: int,
    match_reasons: list[str],
) -> ServiceRecommendation:
    return ServiceRecommendation(
        rank=rank,
        post_id=post.post_id,
        post_title=post.title,
        service_id=service.service_id,
        service_name=service.service_name,
        organization=service.organization,
        city=service.city,
        category=service.category,
        score=score,
        match_reasons=match_reasons,
    )


def build_recommendations(project_root: Path) -> list[ServiceRecommendation]:
    links = build_service_links(project_root)
    posts = {
        post.post_id: post
        for post in load_reddit_posts(project_root)
    }
    services = {
        service.service_id: service
        for service in load_community_services(project_root)
    }

    sorted_links = sorted(
        links,
        key=lambda link: (-link.score, link.post_id, link.service_id),
    )

    recommendations: list[ServiceRecommendation] = []

    for rank, link in enumerate(sorted_links, start=1):
        recommendations.append(
            _build_recommendation(
                rank,
                posts[link.post_id],
                services[link.service_id],
                score=link.score,
                match_reasons=link.match_reasons,
            )
        )

    return recommendations


def build_post_recommendations(
    project_root: Path,
    post_id: str,
    *,
    limit: int = 5,
) -> list[ServiceRecommendation]:
    links = build_service_links(project_root)
    posts = {
        post.post_id: post
        for post in load_reddit_posts(project_root)
    }
    services = {
        service.service_id: service
        for service in load_community_services(project_root)
    }

    post_links = [
        link
        for link in links
        if link.post_id == post_id
    ]

    recommendations: list[ServiceRecommendation] = []

    for rank, link in enumerate(post_links[:limit], start=1):
        recommendations.append(
            _build_recommendation(
                rank,
                posts[link.post_id],
                services[link.service_id],
                score=link.score,
                match_reasons=link.match_reasons,
            )
        )

    return recommendations
