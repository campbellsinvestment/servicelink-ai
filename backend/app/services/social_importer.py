from pathlib import Path

from backend.app.importers.social_adapters import RedditPostAdapter
from backend.app.models.social_post import NormalizedSocialPost
from backend.app.services.enrichment import enrich_social_post
from backend.app.services.organizations import (
    load_organization_registry,
    resolve_project_root,
)


def import_reddit_posts(
    file_path: str | Path,
) -> list[NormalizedSocialPost]:
    path = Path(file_path)
    posts = RedditPostAdapter().import_file(path)
    organization_registry = load_organization_registry(
        resolve_project_root(path),
    )

    return [
        enrich_social_post(post, organization_registry)
        for post in posts
    ]