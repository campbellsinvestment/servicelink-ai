from pathlib import Path

import pandas as pd
import pytest

from backend.app.importers.service_adapters import (
    CommunityServiceAdapter,
    InformAlbertaServiceAdapter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_informalberta_adapter_imports_records() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "informalberta_services.csv"
    )

    records = InformAlbertaServiceAdapter().import_file(file_path)

    assert len(records) == 3
    assert records[0].source == "InformAlberta"
    assert records[0].service_id == "informalberta-1"


def test_community_adapter_imports_records() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "services"
        / "community_services.csv"
    )

    records = CommunityServiceAdapter().import_file(file_path)

    assert len(records) == 3
    assert records[0].source == "Community Services"
    assert records[0].phone == "780-555-0201"


def test_adapter_rejects_missing_columns(tmp_path: Path) -> None:
    file_path = tmp_path / "invalid.csv"

    dataframe = pd.DataFrame(
        [
            {
                "id": 1,
                "service_name": "Transportation",
            }
        ]
    )

    dataframe.to_csv(file_path, index=False)

    with pytest.raises(ValueError, match="Missing required CSV columns"):
        InformAlbertaServiceAdapter().import_file(file_path)


def test_adapter_rejects_missing_file() -> None:
    with pytest.raises(FileNotFoundError, match="CSV file not found"):
        InformAlbertaServiceAdapter().import_file("missing.csv")