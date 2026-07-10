import pandas as pd

from backend.app.importers.base import CSVAdapter
from backend.app.models.service import NormalizedService
from backend.app.services.cleaning import clean_text, normalize_phone
from backend.app.services.geography import normalize_alberta_location
from backend.app.services.taxonomy import normalize_category


class InformAlbertaServiceAdapter(CSVAdapter[NormalizedService]):
    required_columns = {
        "id",
        "organization_name",
        "service_name",
        "category",
        "city",
    }

    def transform_row(self, row: pd.Series) -> NormalizedService:
        city = str(row["city"]).strip()
        geography = normalize_alberta_location(city)

        return NormalizedService(
            service_id=f"informalberta-{row['id']}",
            organization=str(row["organization_name"]).strip(),
            service_name=str(row["service_name"]).strip(),
            category=normalize_category(str(row["category"])),
            city=geography.city if geography else city,
            geography=geography,
            address=clean_text(row.get("address")),
            phone=normalize_phone(row.get("phone")),
            description=clean_text(row.get("description")),
            source="InformAlberta",
            source_record_id=str(row["id"]),
        )


class CommunityServiceAdapter(CSVAdapter[NormalizedService]):
    required_columns = {
        "service_code",
        "provider",
        "title",
        "service_type",
        "municipality",
    }

    def transform_row(self, row: pd.Series) -> NormalizedService:
        city = str(row["municipality"]).strip()
        geography = normalize_alberta_location(city)

        return NormalizedService(
            service_id=f"community-{row['service_code']}",
            organization=str(row["provider"]).strip(),
            service_name=str(row["title"]).strip(),
            category=normalize_category(str(row["service_type"])),
            city=geography.city if geography else city,
            geography=geography,
            address=clean_text(row.get("street_address")),
            phone=normalize_phone(row.get("telephone")),
            description=clean_text(row.get("details")),
            source="Community Services",
            source_record_id=str(row["service_code"]),
        )