from pathlib import Path

import pandas as pd
import pytest

from backend.app.importers.job_adapters import (
    IndeedJobAdapter,
    ZipRecruiterJobAdapter,
    combine_location,
    parse_job_datetime,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_combine_location() -> None:
    assert combine_location(
        "Edmonton",
        "AB",
    ) == "Edmonton, AB"

    assert combine_location(
        "Edmonton",
        None,
    ) == "Edmonton"

    assert combine_location(None, None) is None


def test_parse_job_datetime() -> None:
    result = parse_job_datetime("2026-05-10")

    assert result is not None
    assert result.year == 2026


def test_indeed_adapter_imports_jobs() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "indeed_jobs.csv"
    )

    jobs = IndeedJobAdapter().import_file(file_path)

    assert len(jobs) == 3

    first_job = jobs[0]

    assert first_job.posting_id == "indeed-i001"
    assert first_job.source == "Indeed"
    assert first_job.employer == "Alberta Distribution Ltd"
    assert first_job.location == "Edmonton, AB"
    assert first_job.geography is not None
    assert first_job.geography.city == "Edmonton"


def test_ziprecruiter_adapter_imports_jobs() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "ziprecruiter_jobs.csv"
    )

    jobs = ZipRecruiterJobAdapter().import_file(file_path)

    assert len(jobs) == 3

    first_job = jobs[0]

    assert first_job.posting_id == "ziprecruiter-z001"
    assert first_job.source == "ZipRecruiter"
    assert first_job.location == "Stony Plain, AB"
    assert first_job.geography is not None
    assert first_job.geography.city == "Stony Plain"


def test_indeed_adapter_rejects_missing_columns(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "invalid_indeed.csv"

    dataframe = pd.DataFrame(
        [
            {
                "job_id": "i001",
                "job_title": "Developer",
            }
        ]
    )

    dataframe.to_csv(file_path, index=False)

    with pytest.raises(
        ValueError,
        match="Missing required CSV columns",
    ):
        IndeedJobAdapter().import_file(file_path)