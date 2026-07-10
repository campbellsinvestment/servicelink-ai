CATEGORY_ALIASES = {
    "transportation": {
        "transportation",
        "senior transport",
        "transport",
        "transportation help",
    },
    "food_support": {
        "food support",
        "meal assistance",
        "meal delivery",
        "meals on wheels",
    },
    "home_care": {
        "home care",
        "in-home care",
        "in home care",
        "home care assistance",
    },
}


def normalize_category(value: str) -> str:
    cleaned_value = value.strip().lower()

    for normalized_category, aliases in CATEGORY_ALIASES.items():
        if cleaned_value in aliases:
            return normalized_category

    return "other"