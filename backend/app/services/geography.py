import re

from backend.app.models.geography import AlbertaLocation


ALBERTA_LOCATIONS: dict[str, AlbertaLocation] = {
    "edmonton": AlbertaLocation(
        city="Edmonton",
        latitude=53.5461,
        longitude=-113.4938,
    ),
    "stony plain": AlbertaLocation(
        city="Stony Plain",
        latitude=53.5264,
        longitude=-114.0060,
    ),
    "spruce grove": AlbertaLocation(
        city="Spruce Grove",
        latitude=53.5451,
        longitude=-113.9008,
    ),
    "parkland county": AlbertaLocation(
        city="Parkland County",
        latitude=53.5653,
        longitude=-114.0657,
    ),
}


PROVINCE_VALUES = {
    "ab",
    "alberta",
    "canada",
}


def clean_location_text(value: str | None) -> str | None:
    if not value:
        return None

    cleaned = value.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)

    parts = [
        part.strip()
        for part in cleaned.split(",")
        if part.strip()
    ]

    filtered_parts = [
        part
        for part in parts
        if part not in PROVINCE_VALUES
    ]

    if not filtered_parts:
        return None

    return filtered_parts[0]


def normalize_alberta_location(
    value: str | None,
) -> AlbertaLocation | None:
    cleaned = clean_location_text(value)

    if not cleaned:
        return None

    return ALBERTA_LOCATIONS.get(cleaned)


def format_location(
    location: AlbertaLocation | None,
) -> str | None:
    if location is None:
        return None

    return f"{location.city}, {location.province_code}"