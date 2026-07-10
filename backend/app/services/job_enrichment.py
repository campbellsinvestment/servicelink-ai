"""Deterministic enrichment for normalized job postings."""

from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.services.lexical import (
    extract_keywords,
    extract_locations,
    extract_service_categories,
)
from backend.app.services.organizations import extract_organizations


def _build_analysis_text(job: NormalizedJobPosting) -> str:
    parts = [
        value
        for value in (job.title, job.description, job.location, job.employer)
        if value
    ]

    return " ".join(parts)


def enrich_job_posting(
    job: NormalizedJobPosting,
    organization_registry: list[str] | None = None,
) -> NormalizedJobPosting:
    """Populate lexical enrichment fields on a job posting."""

    analysis_text = _build_analysis_text(job)
    locations = extract_locations(analysis_text)

    if job.geography and job.geography.city not in locations:
        locations.append(job.geography.city)

    update = {
        "locations": locations,
        "service_categories": extract_service_categories(analysis_text),
        "keywords": extract_keywords(analysis_text),
    }

    if organization_registry is not None:
        update["organizations"] = extract_organizations(
            analysis_text,
            organization_registry,
        )

    return job.model_copy(update=update)
