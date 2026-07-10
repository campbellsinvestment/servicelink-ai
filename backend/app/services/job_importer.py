from pathlib import Path

from backend.app.importers.job_adapters import (
    IndeedJobAdapter,
    ZipRecruiterJobAdapter,
)
from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.services.job_enrichment import enrich_job_posting
from backend.app.services.organizations import (
    load_organization_registry,
    resolve_project_root,
)


def import_indeed_jobs(
    file_path: str | Path,
) -> list[NormalizedJobPosting]:
    return IndeedJobAdapter().import_file(file_path)


def import_ziprecruiter_jobs(
    file_path: str | Path,
) -> list[NormalizedJobPosting]:
    return ZipRecruiterJobAdapter().import_file(file_path)


def load_job_postings(project_root: Path) -> list[NormalizedJobPosting]:
    indeed_path = (
        project_root
        / "datasets"
        / "raw"
        / "social"
        / "indeed_jobs.csv"
    )
    ziprecruiter_path = (
        project_root
        / "datasets"
        / "raw"
        / "social"
        / "ziprecruiter_jobs.csv"
    )

    jobs = [
        *import_indeed_jobs(indeed_path),
        *import_ziprecruiter_jobs(ziprecruiter_path),
    ]
    organization_registry = load_organization_registry(project_root)

    return [
        enrich_job_posting(job, organization_registry)
        for job in jobs
    ]
