from datetime import timezone
from pathlib import Path

import pandas as pd
import pytest

from backend.app.importers.social_adapters import (
    RedditPostAdapter,
    combine_post_text,
    parse_datetime,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_combine_post_text() -> None:
    result = combine_post_text(
        "Transportation help",
        "My mother needs a ride.",
    )

    assert result == (
        "Transportation help My mother needs a ride."
    )


def test_combine_post_text_handles_missing_title() -> None:
    result = combine_post_text(
        None,
        "My mother needs a ride.",
    )

    assert result == "My mother needs a ride."


def test_parse_datetime() -> None:
    result = parse_datetime("2026-05-12T14:30:00Z")

    assert result is not None
    assert result.year == 2026
    assert result.month == 5
    assert result.tzinfo == timezone.utc


def test_parse_datetime_handles_invalid_value() -> None:
    assert parse_datetime("not-a-date") is None
    assert parse_datetime(None) is None


def test_reddit_adapter_imports_posts() -> None:
    file_path = (
        PROJECT_ROOT
        / "datasets"
        / "raw"
        / "social"
        / "reddit_posts.csv"
    )

    posts = RedditPostAdapter().import_file(file_path)

    assert len(posts) == 5

    first_post = posts[0]

    assert first_post.post_id == "reddit-r001"
    assert first_post.source == "Reddit"
    assert first_post.community == "Edmonton"
    assert first_post.author == "caregiver123"

    assert "Transportation help" in first_post.body
    assert "medical appointments" in first_post.body

    assert first_post.created_at is not None


def test_reddit_adapter_rejects_missing_columns(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "invalid_reddit.csv"

    dataframe = pd.DataFrame(
        [
            {
                "post_id": "r001",
                "post_title": "Help needed",
            }
        ]
    )

    dataframe.to_csv(file_path, index=False)

    with pytest.raises(
        ValueError,
        match="Missing required CSV columns",
    ):
        RedditPostAdapter().import_file(file_path)