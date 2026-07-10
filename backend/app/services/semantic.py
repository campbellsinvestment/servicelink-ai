"""Lightweight TF-IDF semantic similarity for service search."""

from __future__ import annotations

import math
import re
from collections import Counter

from backend.app.models.service import NormalizedService
from backend.app.services.scoring import STOP_WORDS

SEMANTIC_SCORE_SCALE = 15
SEMANTIC_MATCH_THRESHOLD = 0.08


def tokenize_document(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 2 and token not in STOP_WORDS
    ]


def service_document(service: NormalizedService) -> str:
    return " ".join(
        value
        for value in (
            service.service_name,
            service.description,
            service.category.replace("_", " "),
            service.city,
            service.organization,
        )
        if value
    )


def _term_frequencies(tokens: list[str]) -> dict[str, float]:
    counts = Counter(tokens)
    total = float(len(tokens)) or 1.0

    return {
        term: count / total
        for term, count in counts.items()
    }


def _idf_weights(documents: list[list[str]]) -> dict[str, float]:
    document_count = len(documents) or 1
    document_frequency: Counter[str] = Counter()

    for tokens in documents:
        document_frequency.update(set(tokens))

    return {
        term: math.log((1 + document_count) / (1 + frequency)) + 1.0
        for term, frequency in document_frequency.items()
    }


def _tfidf_vector(
    tokens: list[str],
    idf: dict[str, float],
) -> dict[str, float]:
    frequencies = _term_frequencies(tokens)

    return {
        term: frequency * idf.get(term, 0.0)
        for term, frequency in frequencies.items()
        if term in idf
    }


def _cosine_similarity(
    left: dict[str, float],
    right: dict[str, float],
) -> float:
    if not left or not right:
        return 0.0

    shared = set(left) & set(right)

    if not shared:
        return 0.0

    dot = sum(left[term] * right[term] for term in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    return dot / (left_norm * right_norm)


def semantic_similarity_scores(
    query: str,
    services: list[NormalizedService],
) -> dict[str, float]:
    """Return cosine similarity of the query against each service document."""

    service_tokens = [
        tokenize_document(service_document(service))
        for service in services
    ]
    query_tokens = tokenize_document(query)
    idf = _idf_weights([*service_tokens, query_tokens])
    query_vector = _tfidf_vector(query_tokens, idf)

    scores: dict[str, float] = {}

    for service, tokens in zip(services, service_tokens, strict=True):
        scores[service.service_id] = _cosine_similarity(
            query_vector,
            _tfidf_vector(tokens, idf),
        )

    return scores


def semantic_bonus(similarity: float) -> tuple[int, str | None]:
    """Convert cosine similarity into an explainable integer score bonus."""

    if similarity < SEMANTIC_MATCH_THRESHOLD:
        return 0, None

    points = max(1, round(similarity * SEMANTIC_SCORE_SCALE))

    return points, f"semantic:{similarity:.2f}"
