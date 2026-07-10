from pathlib import Path

from backend.app.importers.job_adapters import (
    IndeedJobAdapter,
    ZipRecruiterJobAdapter,
)
from backend.app.models.job_posting import NormalizedJobPosting


def import_indeed_jobs(
    file_path: str | Path,
) -> list[NormalizedJobPosting]:
    return IndeedJobAdapter().import_file(file_path)


def import_ziprecruiter_jobs(
    file_path: str | Path,
) -> list[NormalizedJobPosting]:
    return ZipRecruiterJobAdapter().import_file(file_path)