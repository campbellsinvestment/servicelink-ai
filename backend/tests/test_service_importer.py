from pathlib import Path

from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
    normalize_phone,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_normalize_phone() -> None:
    assert normalize_phone("7805550201") == "780-555-0201"
    assert normalize_phone("780-555-0201") == "780-555-0201"
    assert normalize_phone(None) is None


def test_import_informalberta_services() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "informalberta_services.csv"
    )

    services = import_informalberta_services(file_path)

    assert len(services) == 3
    assert services[0].source == "InformAlberta"
    assert services[0].category == "transportation"
    assert services[0].city == "Edmonton"


def test_import_community_services() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "community_services.csv"
    )

    services = import_community_services(file_path)

    assert len(services) == 3
    assert services[0].source == "Community Services"
    assert services[0].category == "transportation"
    assert services[0].phone == "780-555-0201"