from backend.app.models.service import NormalizedService
from backend.app.services.organizations import (
    collect_organization_names,
    extract_organizations,
)


ORGANIZATION_REGISTRY = [
    "Parkland Community Support",
    "Edmonton Senior Resources",
    "Edmonton Seniors Centre",
    "Alberta Wellness Network",
    "Spruce Grove Care Society",
    "West Park Outreach",
]


def test_collect_organization_names_returns_unique_sorted_values() -> None:
    services = [
        NormalizedService(
            service_id="informalberta-1",
            organization="Edmonton Seniors Centre",
            service_name="Senior Transportation",
            category="transportation",
            city="Edmonton",
            source="InformAlberta",
            source_record_id="1",
        ),
        NormalizedService(
            service_id="community-A101",
            organization="Edmonton Senior Resources",
            service_name="Transportation Help",
            category="transportation",
            city="Edmonton",
            source="Community Services",
            source_record_id="A101",
        ),
        NormalizedService(
            service_id="informalberta-1-duplicate",
            organization="Edmonton Seniors Centre",
            service_name="Duplicate",
            category="transportation",
            city="Edmonton",
            source="InformAlberta",
            source_record_id="1b",
        ),
    ]

    organizations = collect_organization_names(services)

    assert organizations == [
        "Edmonton Senior Resources",
        "Edmonton Seniors Centre",
    ]


def test_extract_organizations_finds_longest_matching_names() -> None:
    text = (
        "Has anyone used Edmonton Seniors Centre for affordable "
        "transportation to medical appointments?"
    )

    organizations = extract_organizations(text, ORGANIZATION_REGISTRY)

    assert organizations == ["Edmonton Seniors Centre"]


def test_extract_organizations_returns_multiple_matches_in_text_order() -> None:
    text = (
        "West Park Outreach and Edmonton Senior Resources both offer "
        "helpful community programs."
    )

    organizations = extract_organizations(text, ORGANIZATION_REGISTRY)

    assert organizations == [
        "West Park Outreach",
        "Edmonton Senior Resources",
    ]


def test_extract_organizations_returns_empty_when_no_names_match() -> None:
    organizations = extract_organizations(
        "Looking for warehouse employment near Stony Plain.",
        ORGANIZATION_REGISTRY,
    )

    assert organizations == []
