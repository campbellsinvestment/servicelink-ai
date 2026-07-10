from datetime import datetime

import pandas as pd

from backend.app.importers.base import CSVAdapter
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.cleaning import clean_text


def parse_datetime(value: object) -> datetime | None:
    """Convert a source date value into a Python datetime."""

    if pd.isna(value):
        return None

    parsed = pd.to_datetime(value, errors="coerce", utc=True)

    if pd.isna(parsed):
        return None

    return parsed.to_pydatetime()


def combine_post_text(
    title: object,
    body: object,
) -> str:
    """Combine a post title and body into searchable text."""

    cleaned_title = clean_text(title)
    cleaned_body = clean_text(body)

    parts = [
        value
        for value in (cleaned_title, cleaned_body)
        if value
    ]

    return " ".join(parts)


class RedditPostAdapter(CSVAdapter[NormalizedSocialPost]):
    required_columns = {
        "post_id",
        "subreddit",
        "post_title",
        "post_text",
    }

    def transform_row(
        self,
        row: pd.Series,
    ) -> NormalizedSocialPost:
        source_record_id = str(row["post_id"]).strip()
        title = clean_text(row.get("post_title"))
        post_text = clean_text(row.get("post_text"))

        combined_text = combine_post_text(title, post_text)

        return NormalizedSocialPost(
            post_id=f"reddit-{source_record_id}",
            source="Reddit",
            source_record_id=source_record_id,
            title=title,
            body=combined_text,
            author=clean_text(row.get("username")),
            community=clean_text(row.get("subreddit")),
            url=clean_text(row.get("permalink")),
            created_at=parse_datetime(row.get("created_utc")),
        )