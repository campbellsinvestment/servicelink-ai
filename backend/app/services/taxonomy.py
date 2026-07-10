CATEGORY_ALIASES = {
    "transportation": {
        "transportation",
        "senior transport",
        "transport",
        "transportation help",
        "rides",
        "ride",
        "medical appointments",
    },
    "food_support": {
        "food support",
        "meal assistance",
        "meal delivery",
        "meals on wheels",
        "deliver meals",
        "meal",
        "meals",
        "food",
    },
    "home_care": {
        "home care",
        "in-home care",
        "in home care",
        "home care assistance",
        "in-home assistance",
        "home care assistant",
        "community support worker",
        "daily living",
        "caregiver",
        "in home support",
        "in-home support",
    },
}


def normalize_category(value: str) -> str:
    cleaned_value = value.strip().lower()

    for normalized_category, aliases in CATEGORY_ALIASES.items():
        if cleaned_value in aliases:
            return normalized_category

    return "other"