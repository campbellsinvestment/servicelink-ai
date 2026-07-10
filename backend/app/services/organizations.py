"""Deterministic organization extraction and registry helpers."""

from pathlib import Path

from backend.app.models.service import NormalizedService
from backend.app.services.service_importer import (
    import_community_services,
    import_informalberta_services,
)


def collect_organization_names(
    services: list[NormalizedService],
) -> list[str]:
    """Return unique organization names sorted longest-first for matching."""

    organizations = {
        service.organization.strip()
        for service in services
        if service.organization.strip()
    }

    return sorted(organizations, key=len, reverse=True)


def extract_organizations(
    text: str,
    organization_registry: list[str],
) -> list[str]:
    """Return organization names mentioned in text."""

    normalized = text.lower()
    matches: list[tuple[int, str]] = []

    for organization in organization_registry:
        index = normalized.find(organization.lower())

        if index == -1:
            continue

        matches.append((index, organization))

    matches.sort(key=lambda item: item[0])

    organizations: list[str] = []

    for _, organization in matches:
        if organization not in organizations:
            organizations.append(organization)

    return organizations


def load_organization_registry(project_root: Path) -> list[str]:
    """Build an organization registry from normalized service records."""

    informalberta_path = (
        project_root
        / "datasets"
        / "raw"
        / "services"
        / "informalberta_services.csv"
    )
    community_path = (
        project_root
        / "datasets"
        / "raw"
        / "services"
        / "community_services.csv"
    )

    services = [
        *import_informalberta_services(informalberta_path),
        *import_community_services(community_path),
    ]

    return collect_organization_names(services)


def resolve_project_root(dataset_path: Path) -> Path:
    """Resolve the repository root from a datasets/raw/* file path."""

    return dataset_path.resolve().parents[3]
