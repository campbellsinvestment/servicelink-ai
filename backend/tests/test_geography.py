from backend.app.services.geography import (
    clean_location_text,
    format_location,
    normalize_alberta_location,
)


def test_clean_location_text() -> None:
    assert clean_location_text("Edmonton, AB") == "edmonton"
    assert clean_location_text("Edmonton, Alberta") == "edmonton"
    assert clean_location_text("  Spruce Grove  ") == "spruce grove"


def test_normalize_edmonton() -> None:
    location = normalize_alberta_location("Edmonton, Alberta")

    assert location is not None
    assert location.city == "Edmonton"
    assert location.province_code == "AB"
    assert location.latitude == 53.5461


def test_normalize_stony_plain() -> None:
    location = normalize_alberta_location("Stony Plain, AB")

    assert location is not None
    assert location.city == "Stony Plain"


def test_unknown_location_returns_none() -> None:
    assert normalize_alberta_location("Toronto, Ontario") is None


def test_format_location() -> None:
    location = normalize_alberta_location("Spruce Grove, Alberta")

    assert format_location(location) == "Spruce Grove, AB"