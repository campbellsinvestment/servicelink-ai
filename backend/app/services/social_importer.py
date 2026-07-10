from pathlib import Path

from backend.app.importers.social_adapters import RedditPostAdapter
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.enrichment import enrich_social_post


def import_reddit_posts(
    file_path: str | Path,
) -> list[NormalizedSocialPost]:
    posts = RedditPostAdapter().import_file(file_path)

    return [enrich_social_post(post) for post in posts]