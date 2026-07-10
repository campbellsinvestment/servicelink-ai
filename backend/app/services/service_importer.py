from pathlib import Path

from backend.app.importers.service_adapters import (
    CommunityServiceAdapter,
    InformAlbertaServiceAdapter,
)
from backend.app.models.service import NormalizedService
from backend.app.services.cleaning import clean_text, normalize_phone


def import_informalberta_services(
    file_path: str | Path,
) -> list[NormalizedService]:
    return InformAlbertaServiceAdapter().import_file(file_path)


def import_community_services(
    file_path: str | Path,
) -> list[NormalizedService]:
    return CommunityServiceAdapter().import_file(file_path)


__all__ = [
    "clean_text",
    "normalize_phone",
    "import_informalberta_services",
    "import_community_services",
]