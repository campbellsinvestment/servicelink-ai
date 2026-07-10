from pathlib import Path

import pytest

from backend.app.services.job_enrichment import enrich_job_posting
from backend.app.services.job_importer import load_job_postings
from backend.app.services.job_linking import (
    build_job_service_links,
    link_job_to_services,
)
from backend.app.services.entity_linking import load_community_services


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_enrich_job_posting_extracts_categories_and_locations() -> None:
    jobs = load_job_postings(PROJECT_ROOT)
    meal_delivery_job = next(
        job for job in jobs if job.source_record_id == "z001"
    )

    assert "food_support" in meal_delivery_job.service_categories
    assert "Stony Plain" in meal_delivery_job.locations


def test_link_job_to_services_returns_explainable_matches() -> None:
    jobs = load_job_postings(PROJECT_ROOT)
    services = load_community_services(PROJECT_ROOT)
    home_care_job = next(
        job for job in jobs if job.source_record_id == "z003"
    )

    links = link_job_to_services(home_care_job, services)

    assert links
    assert links[0].score >= links[-1].score
    assert links[0].match_reasons[0].startswith("category:")


def test_build_job_service_links_returns_ranked_demo_matches() -> None:
    links = build_job_service_links(PROJECT_ROOT)

    assert len(links) == 4
    assert links[0].score >= links[-1].score


def test_warehouse_job_returns_no_service_links() -> None:
    jobs = load_job_postings(PROJECT_ROOT)
    services = load_community_services(PROJECT_ROOT)
    warehouse_job = next(
        job for job in jobs if job.source_record_id == "i001"
    )

    links = link_job_to_services(warehouse_job, services)

    assert links == []
