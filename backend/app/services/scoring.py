"""Explainable recommendation scoring for service matches."""

import re

from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.models.service import NormalizedService
from backend.app.models.social_post import NormalizedSocialPost


CATEGORY_MATCH_SCORE = 10
LOCATION_MATCH_SCORE = 5
CATEGORY_ONLY_MATCH_SCORE = 5
KEYWORD_OVERLAP_SCORE = 3
ORGANIZATION_MATCH_SCORE = 8

SOURCE_TRUST_SCORES: dict[str, int] = {
    "InformAlberta": 5,
    "Community Services": 2,
}

STOP_WORDS = {
    "about",
    "after",
    "also",
    "any",
    "are",
    "can",
    "for",
    "from",
    "has",
    "have",
    "help",
    "her",
    "his",
    "how",
    "into",
    "its",
    "just",
    "like",
    "living",
    "need",
    "needs",
    "old",
    "one",
    "our",
    "out",
    "she",
    "that",
    "the",
    "their",
    "them",
    "there",
    "these",
    "they",
    "this",
    "through",
    "very",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "your",
}


def tokenize(text: str) -> set[str]:
    """Extract meaningful lowercase tokens from text."""

    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 3 and token not in STOP_WORDS
    }

    return tokens


def find_keyword_overlap(
    post: NormalizedSocialPost,
    service: NormalizedService,
) -> tuple[int, list[str]]:
    """Score shared terms between a post and a service description."""

    return find_keyword_overlap_from_text(post.body, service)


def find_keyword_overlap_from_text(
    text: str,
    service: NormalizedService,
) -> tuple[int, list[str]]:
    """Score shared terms between text and a service description."""

    text_tokens = tokenize(text)

    service_text = " ".join(
        value
        for value in (service.service_name, service.description)
        if value
    )
    service_tokens = tokenize(service_text)

    shared_keywords = sorted(text_tokens & service_tokens)
    score = len(shared_keywords) * KEYWORD_OVERLAP_SCORE

    return score, shared_keywords


def source_trust_bonus(service: NormalizedService) -> tuple[int, str | None]:
    """Apply a small bonus for trusted source registries."""

    score = SOURCE_TRUST_SCORES.get(service.source, 0)

    if score == 0:
        return 0, None

    return score, f"source:{service.source}"


def organization_match_bonus(
    post: NormalizedSocialPost,
    service: NormalizedService,
) -> tuple[int, str | None]:
    """Reward links when a post explicitly mentions the service provider."""

    if service.organization not in post.organizations:
        return 0, None

    return (
        ORGANIZATION_MATCH_SCORE,
        f"organization:{service.organization}",
    )


def score_service_match(
    post: NormalizedSocialPost,
    service: NormalizedService,
    *,
    has_location_match: bool,
) -> tuple[int, list[str]]:
    """Build an explainable score for a post-to-service match."""

    if post.locations:
        score = CATEGORY_MATCH_SCORE
        match_reasons = [f"category:{service.category}"]

        if has_location_match:
            score += LOCATION_MATCH_SCORE
            match_reasons.append(f"city:{service.city}")
    else:
        score = CATEGORY_ONLY_MATCH_SCORE
        match_reasons = [f"category:{service.category}"]

    keyword_score, shared_keywords = find_keyword_overlap(post, service)

    if keyword_score:
        score += keyword_score
        match_reasons.append(f"keywords:{','.join(shared_keywords)}")

    source_score, source_reason = source_trust_bonus(service)

    if source_reason:
        score += source_score
        match_reasons.append(source_reason)

    organization_score, organization_reason = organization_match_bonus(
        post,
        service,
    )

    if organization_reason:
        score += organization_score
        match_reasons.append(organization_reason)

    return score, match_reasons


def organization_match_bonus_for_names(
    organization_names: list[str],
    service: NormalizedService,
) -> tuple[int, str | None]:
    """Reward links when text explicitly mentions the service provider."""

    if service.organization not in organization_names:
        return 0, None

    return (
        ORGANIZATION_MATCH_SCORE,
        f"organization:{service.organization}",
    )


def score_job_service_match(
    job: NormalizedJobPosting,
    service: NormalizedService,
    *,
    has_location_match: bool,
) -> tuple[int, list[str]]:
    """Build an explainable score for a job-to-service match."""

    if job.locations:
        score = CATEGORY_MATCH_SCORE
        match_reasons = [f"category:{service.category}"]

        if has_location_match:
            score += LOCATION_MATCH_SCORE
            match_reasons.append(f"city:{service.city}")
    else:
        score = CATEGORY_ONLY_MATCH_SCORE
        match_reasons = [f"category:{service.category}"]

    job_text = " ".join(
        value
        for value in (job.title, job.description)
        if value
    )
    keyword_score, shared_keywords = find_keyword_overlap_from_text(
        job_text,
        service,
    )

    if keyword_score:
        score += keyword_score
        match_reasons.append(f"keywords:{','.join(shared_keywords)}")

    source_score, source_reason = source_trust_bonus(service)

    if source_reason:
        score += source_score
        match_reasons.append(source_reason)

    organization_score, organization_reason = organization_match_bonus_for_names(
        job.organizations,
        service,
    )

    if organization_reason:
        score += organization_score
        match_reasons.append(organization_reason)

    return score, match_reasons
