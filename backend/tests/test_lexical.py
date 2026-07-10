from backend.app.services.lexical import (
    extract_keywords,
    extract_locations,
    extract_service_categories,
)


TRANSPORTATION_POST = (
    "Transportation help for my mother My 78 year old mother needs "
    "affordable transportation to medical appointments in Edmonton."
)

MEAL_DELIVERY_POST = (
    "Meal delivery options Looking for meal delivery or food support "
    "services for an older adult living alone."
)

HOME_CARE_POST = (
    "Home care services Can anyone recommend an organization providing "
    "in-home care for seniors in Spruce Grove?"
)

JOB_SEARCH_POST = (
    "Looking for warehouse employment Are there any employers hiring "
    "warehouse workers near Stony Plain or Spruce Grove?"
)


def test_extract_service_categories_from_transportation_post() -> None:
    categories = extract_service_categories(TRANSPORTATION_POST)

    assert categories == ["transportation"]


def test_extract_service_categories_from_meal_delivery_post() -> None:
    categories = extract_service_categories(MEAL_DELIVERY_POST)

    assert categories == ["food_support"]


def test_extract_service_categories_from_home_care_post() -> None:
    categories = extract_service_categories(HOME_CARE_POST)

    assert categories == ["home_care"]


def test_extract_service_categories_returns_empty_for_unrelated_text() -> None:
    categories = extract_service_categories(JOB_SEARCH_POST)

    assert categories == []


def test_extract_locations_from_transportation_post() -> None:
    locations = extract_locations(TRANSPORTATION_POST)

    assert locations == ["Edmonton"]


def test_extract_locations_from_job_search_post() -> None:
    locations = extract_locations(JOB_SEARCH_POST)

    assert locations == ["Stony Plain", "Spruce Grove"]


def test_extract_keywords_from_transportation_post() -> None:
    keywords = extract_keywords(TRANSPORTATION_POST)

    assert "transportation" in keywords
    assert "transportation help" in keywords
    assert "edmonton" in keywords


def test_extract_keywords_from_home_care_post() -> None:
    keywords = extract_keywords(HOME_CARE_POST)

    assert "in-home care" in keywords
    assert "spruce grove" in keywords
