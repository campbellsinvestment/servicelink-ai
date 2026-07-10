from pathlib import Path

from backend.app.models.job_posting import NormalizedJobPosting
from backend.app.models.service import NormalizedService
from backend.app.services.job_enrichment import enrich_job_posting
from backend.app.services.scoring import score_job_service_match


def test_enrich_job_posting_populates_service_categories() -> None:
    job = NormalizedJobPosting(
        posting_id="ziprecruiter-z003",
        source="ZipRecruiter",
        source_record_id="z003",
        title="Home Care Assistant",
        employer="Spruce Grove Home Supports",
        description="Provide in-home assistance for older adults",
        location="Spruce Grove, AB",
    )

    enriched = enrich_job_posting(job)

    assert enriched.service_categories == ["home_care"]
    assert enriched.locations == ["Spruce Grove"]


def test_score_job_service_match_includes_category_and_city() -> None:
    job = NormalizedJobPosting(
        posting_id="ziprecruiter-z003",
        source="ZipRecruiter",
        source_record_id="z003",
        title="Home Care Assistant",
        employer="Spruce Grove Home Supports",
        description="Provide in-home assistance for older adults",
        location="Spruce Grove, AB",
        locations=["Spruce Grove"],
        service_categories=["home_care"],
    )
    service = NormalizedService(
        service_id="community-A103",
        organization="Spruce Grove Care Society",
        service_name="In Home Support",
        category="home_care",
        city="Spruce Grove",
        description="Personal and household assistance for older adults",
        source="Community Services",
        source_record_id="A103",
    )

    score, reasons = score_job_service_match(
        job,
        service,
        has_location_match=True,
    )

    assert score >= 15
    assert "category:home_care" in reasons
    assert "city:Spruce Grove" in reasons
