from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_job_links_pipeline_connects_jobs_to_services() -> None:
    response = client.get("/job-links")

    assert response.status_code == 200

    links = response.json()

    assert len(links) == 4

    linked_job_ids = {link["posting_id"] for link in links}

    assert linked_job_ids == {
        "ziprecruiter-z001",
        "ziprecruiter-z003",
    }


def test_job_postings_include_enrichment_fields() -> None:
    response = client.get("/job-postings")

    assert response.status_code == 200

    jobs = response.json()
    meal_delivery_job = next(
        job for job in jobs if job["source_record_id"] == "z001"
    )

    assert "food_support" in meal_delivery_job["service_categories"]
    assert "Stony Plain" in meal_delivery_job["locations"]
