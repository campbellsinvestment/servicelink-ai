import pandas as pd


def normalize_phone(value: object) -> str | None:
    if pd.isna(value):
        return None

    digits = "".join(
        character for character in str(value)
        if character.isdigit()
    )

    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return digits or None


def clean_text(value: object) -> str | None:
    if pd.isna(value):
        return None

    cleaned = str(value).strip()
    return cleaned or None