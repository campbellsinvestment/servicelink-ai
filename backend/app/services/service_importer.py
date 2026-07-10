from pathlib import Path

import pandas as pd

from backend.app.models.service import NormalizedService
from backend.app.services.taxonomy import normalize_category


def normalize_phone(value: object) -> str | None:
    if pd.isna(value):
        return None

    digits = "".join(character for character in str(value) if character.isdigit())

    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return digits or None


def clean_text(value: object) -> str | None:
    if pd.isna(value):
        return None

    cleaned = str(value).strip()
    return cleaned or None


def import_informalberta_services(
    file_path: str | Path,
) -> list[NormalizedService]:
    dataframe = pd.read_csv(file_path)

    services: list[NormalizedService] = []

    for _, row in dataframe.iterrows():
        service = NormalizedService(
            service_id=f"informalberta-{row['id']}",
            organization=str(row["organization_name"]).strip(),
            service_name=str(row["service_name"]).strip(),
            category=normalize_category(str(row["category"])),
            city=str(row["city"]).strip(),
            address=clean_text(row.get("address")),
            phone=normalize_phone(row.get("phone")),
            description=clean_text(row.get("description")),
            source="InformAlberta",
            source_record_id=str(row["id"]),
        )

        services.append(service)

    return services


def import_community_services(
    file_path: str | Path,
) -> list[NormalizedService]:
    dataframe = pd.read_csv(file_path)

    services: list[NormalizedService] = []

    for _, row in dataframe.iterrows():
        service = NormalizedService(
            service_id=f"community-{row['service_code']}",
            organization=str(row["provider"]).strip(),
            service_name=str(row["title"]).strip(),
            category=normalize_category(str(row["service_type"])),
            city=str(row["municipality"]).strip(),
            address=clean_text(row.get("street_address")),
            phone=normalize_phone(row.get("telephone")),
            description=clean_text(row.get("details")),
            source="Community Services",
            source_record_id=str(row["service_code"]),
        )

        services.append(service)

    return services