from pathlib import Path

from backend.app.importers.social_adapters import RedditPostAdapter
from backend.app.models.social_post import NormalizedSocialPost


def import_reddit_posts(
    file_path: str | Path,
) -> list[NormalizedSocialPost]:
    return RedditPostAdapter().import_file(file_path)