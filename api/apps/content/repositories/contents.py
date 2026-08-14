from apps.content.models import Content
from common.repositories import BaseRepository


class ContentRepository(BaseRepository[Content]):
    """Data access for the texts of the landing page."""

    model = Content
