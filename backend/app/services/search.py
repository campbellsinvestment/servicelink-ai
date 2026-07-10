"""Conversational search over community services."""

from pathlib import Path

from backend.app.models.search import (
    InterpretedQuery,
    SearchResponse,
    SearchResult,
)
from backend.app.models.service import NormalizedService
from backend.app.services.entity_linking import load_community_services
from backend.app.services.lexical import (
    extract_keywords,
    extract_locations,
    extract_service_categories,
)
from backend.app.services.scoring import (
    CATEGORY_MATCH_SCORE,
    CATEGORY_ONLY_MATCH_SCORE,
    LOCATION_MATCH_SCORE,
    find_keyword_overlap_from_text,
    source_trust_bonus,
)
from backend.app.services.semantic import (
    SEMANTIC_MATCH_THRESHOLD,
    semantic_bonus,
    semantic_similarity_scores,
)


def interpret_query(query: str) -> InterpretedQuery:
    """Extract searchable intent from a natural-language question."""

    cleaned = query.strip()
    categories = extract_service_categories(cleaned)
    locations = extract_locations(cleaned)
    keywords = extract_keywords(cleaned)

    parts: list[str] = []

    if categories:
        readable = ", ".join(category.replace("_", " ") for category in categories)
        parts.append(f"looking for {readable}")

    if locations:
        parts.append(f"in {', '.join(locations)}")

    if not parts and keywords:
        parts.append(f"matching terms: {', '.join(keywords[:5])}")

    if not parts:
        summary = "No clear service category or location detected; using semantic similarity."
    else:
        summary = " ".join(parts)
        summary = summary[0].upper() + summary[1:] + "."

    return InterpretedQuery(
        query=cleaned,
        categories=categories,
        locations=locations,
        keywords=keywords,
        summary=summary,
    )


def score_service_for_query(
    query: InterpretedQuery,
    service: NormalizedService,
    *,
    semantic_similarity: float = 0.0,
) -> tuple[int, list[str]] | None:
    """Score one service against an interpreted conversational query."""

    has_lexical_filters = bool(query.categories or query.locations)

    if query.categories and service.category not in query.categories:
        return None

    score = 0
    match_reasons: list[str] = []

    if query.categories:
        if query.locations:
            score += CATEGORY_MATCH_SCORE
            match_reasons.append(f"category:{service.category}")

            if service.city in query.locations:
                score += LOCATION_MATCH_SCORE
                match_reasons.append(f"city:{service.city}")
            else:
                return None
        else:
            score += CATEGORY_ONLY_MATCH_SCORE
            match_reasons.append(f"category:{service.category}")
    elif query.locations:
        if service.city not in query.locations:
            return None

        score += LOCATION_MATCH_SCORE
        match_reasons.append(f"city:{service.city}")

    keyword_score, shared_keywords = find_keyword_overlap_from_text(
        query.query,
        service,
    )

    if keyword_score:
        score += keyword_score
        match_reasons.append(f"keywords:{','.join(shared_keywords)}")

    semantic_score, semantic_reason = semantic_bonus(semantic_similarity)

    if semantic_reason:
        score += semantic_score
        match_reasons.append(semantic_reason)

    if not match_reasons:
        return None

    if not has_lexical_filters and semantic_similarity < SEMANTIC_MATCH_THRESHOLD:
        return None

    source_score, source_reason = source_trust_bonus(service)

    if source_reason:
        score += source_score
        match_reasons.append(source_reason)

    return score, match_reasons


def build_answer(
    interpretation: InterpretedQuery,
    results: list[SearchResult],
) -> str:
    if not results:
        if interpretation.categories or interpretation.locations:
            return (
                "I could not find a matching community service for that request "
                "in the current demo datasets."
            )

        return (
            "Try asking about transportation, meal delivery, or home care "
            "in Edmonton, Stony Plain, or Spruce Grove."
        )

    top = results[0]
    category = top.category.replace("_", " ")

    if len(results) == 1:
        return (
            f"I found {top.service_name} from {top.organization} "
            f"in {top.city} ({category})."
        )

    return (
        f"I found {len(results)} matching services. "
        f"The strongest match is {top.service_name} from {top.organization} "
        f"in {top.city}."
    )


def search_services(
    project_root: Path,
    query: str,
    *,
    limit: int = 5,
) -> SearchResponse:
    """Answer a natural-language service question with ranked matches."""

    interpretation = interpret_query(query)
    services = load_community_services(project_root)
    similarities = semantic_similarity_scores(interpretation.query, services)
    scored: list[tuple[int, list[str], NormalizedService]] = []

    for service in services:
        result = score_service_for_query(
            interpretation,
            service,
            semantic_similarity=similarities.get(service.service_id, 0.0),
        )

        if result is None:
            continue

        score, match_reasons = result
        scored.append((score, match_reasons, service))

    scored.sort(key=lambda item: (-item[0], item[2].service_id))

    results: list[SearchResult] = []

    for rank, (score, match_reasons, service) in enumerate(
        scored[:limit],
        start=1,
    ):
        results.append(
            SearchResult(
                rank=rank,
                service_id=service.service_id,
                service_name=service.service_name,
                organization=service.organization,
                city=service.city,
                category=service.category,
                score=score,
                match_reasons=match_reasons,
            )
        )

    return SearchResponse(
        interpretation=interpretation,
        results=results,
        answer=build_answer(interpretation, results),
    )
