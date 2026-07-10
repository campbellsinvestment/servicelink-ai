"""Deterministic entity linking between job postings and services."""

from pathlib import Path

from backend.app.models.job_link import JobServiceLink
from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.models.service import NormalizedService
from backend.app.services.entity_linking import load_community_services
from backend.app.services.job_importer import load_job_postings
from backend.app.services.scoring import score_job_service_match


def _city_matches(job: NormalizedJobPosting, service: NormalizedService) -> bool:
    return any(
        location.lower() == service.city.lower()
        for location in job.locations
    )


def link_job_to_services(
    job: NormalizedJobPosting,
    services: list[NormalizedService],
) -> list[JobServiceLink]:
    """Link a job posting to community services using explainable rules."""

    if not job.service_categories:
        return []

    links: list[JobServiceLink] = []

    for service in services:
        if service.category not in job.service_categories:
            continue

        if job.locations:
            if not _city_matches(job, service):
                continue

            score, match_reasons = score_job_service_match(
                job,
                service,
                has_location_match=True,
            )
        else:
            score, match_reasons = score_job_service_match(
                job,
                service,
                has_location_match=False,
            )

        links.append(
            JobServiceLink(
                posting_id=job.posting_id,
                service_id=service.service_id,
                score=score,
                match_reasons=match_reasons,
            )
        )

    links.sort(
        key=lambda link: (-link.score, link.service_id),
    )

    return links


def link_jobs_to_services(
    jobs: list[NormalizedJobPosting],
    services: list[NormalizedService],
) -> list[JobServiceLink]:
    """Link multiple job postings to community services."""

    links: list[JobServiceLink] = []

    for job in jobs:
        links.extend(link_job_to_services(job, services))

    return links


def build_job_service_links(project_root: Path) -> list[JobServiceLink]:
    jobs = load_job_postings(project_root)
    services = load_community_services(project_root)

    links = link_jobs_to_services(jobs, services)
    links.sort(
        key=lambda link: (-link.score, link.posting_id, link.service_id),
    )

    return links
