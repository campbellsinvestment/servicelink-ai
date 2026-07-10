from datetime import datetime

import pandas as pd

from backend.app.importers.base import CSVAdapter
from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.services.cleaning import clean_text
from backend.app.services.geography import (
    format_location,
    normalize_alberta_location,
)


def parse_job_datetime(value: object) -> datetime | None:
    if pd.isna(value):
        return None

    parsed = pd.to_datetime(value, errors="coerce", utc=True)

    if pd.isna(parsed):
        return None

    return parsed.to_pydatetime()


def combine_location(
    city: object,
    province: object,
) -> str | None:
    cleaned_city = clean_text(city)
    cleaned_province = clean_text(province)

    values = [
        value
        for value in (cleaned_city, cleaned_province)
        if value
    ]

    if not values:
        return None

    return ", ".join(values)


class IndeedJobAdapter(CSVAdapter[NormalizedJobPosting]):
    required_columns = {
        "job_id",
        "job_title",
        "company_name",
        "job_description",
    }

    def transform_row(
        self,
        row: pd.Series,
    ) -> NormalizedJobPosting:
        source_id = str(row["job_id"]).strip()

        raw_location = combine_location(
            row.get("city"),
            row.get("province"),
        )
        geography = normalize_alberta_location(raw_location)

        return NormalizedJobPosting(
            posting_id=f"indeed-{source_id}",
            source="Indeed",
            source_record_id=source_id,
            title=str(row["job_title"]).strip(),
            employer=str(row["company_name"]).strip(),
            description=str(row["job_description"]).strip(),
            location=format_location(geography) or raw_location,
            geography=geography,
            employment_type=clean_text(row.get("job_type")),
            salary=clean_text(row.get("salary_text")),
            url=clean_text(row.get("job_url")),
            posted_at=parse_job_datetime(
                row.get("date_posted")
            ),
        )


class ZipRecruiterJobAdapter(
    CSVAdapter[NormalizedJobPosting]
):
    required_columns = {
        "listing_id",
        "title",
        "employer",
        "summary",
    }

    def transform_row(
        self,
        row: pd.Series,
    ) -> NormalizedJobPosting:
        source_id = str(row["listing_id"]).strip()

        raw_location = clean_text(row.get("location_name"))
        geography = normalize_alberta_location(raw_location)

        return NormalizedJobPosting(
            posting_id=f"ziprecruiter-{source_id}",
            source="ZipRecruiter",
            source_record_id=source_id,
            title=str(row["title"]).strip(),
            employer=str(row["employer"]).strip(),
            description=str(row["summary"]).strip(),
            location=format_location(geography) or raw_location,
            geography=geography,
            employment_type=clean_text(
                row.get("work_schedule")
            ),
            salary=clean_text(row.get("compensation")),
            url=clean_text(row.get("apply_link")),
            posted_at=parse_job_datetime(
                row.get("published_date")
            ),
        )