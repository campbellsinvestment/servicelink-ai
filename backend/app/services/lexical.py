"""Rule-based lexical analysis for community-service text."""

from backend.app.services.geography import ALBERTA_LOCATIONS
from backend.app.services.taxonomy import CATEGORY_ALIASES


def _normalize_text(text: str) -> str:
    return text.strip().lower()


def extract_service_categories(text: str) -> list[str]:
    """Return normalized service categories mentioned in text."""

    normalized = _normalize_text(text)
    categories: list[str] = []

    for category, aliases in CATEGORY_ALIASES.items():
        for alias in sorted(aliases, key=len, reverse=True):
            if alias in normalized:
                categories.append(category)
                break

    return categories


def extract_locations(text: str) -> list[str]:
    """Return canonical Alberta city names mentioned in text."""

    normalized = _normalize_text(text)
    matches: list[tuple[int, str]] = []

    for location_key in sorted(
        ALBERTA_LOCATIONS.keys(),
        key=len,
        reverse=True,
    ):
        start = 0
        while True:
            index = normalized.find(location_key, start)
            if index == -1:
                break

            city = ALBERTA_LOCATIONS[location_key].city
            matches.append((index, city))
            start = index + len(location_key)

    matches.sort(key=lambda item: item[0])

    locations: list[str] = []
    for _, city in matches:
        if city not in locations:
            locations.append(city)

    return locations


def extract_keywords(text: str) -> list[str]:
    """Return matched category aliases and location phrases from text."""

    normalized = _normalize_text(text)
    keywords: list[str] = []

    aliases = {
        alias
        for aliases in CATEGORY_ALIASES.values()
        for alias in aliases
    }

    for alias in sorted(aliases, key=len, reverse=True):
        if alias in normalized and alias not in keywords:
            keywords.append(alias)

    for location_key in sorted(
        ALBERTA_LOCATIONS.keys(),
        key=len,
        reverse=True,
    ):
        if location_key in normalized and location_key not in keywords:
            keywords.append(location_key)

    return keywords
