from apps.site_config.models import SiteConfig
from common.repositories import BaseRepository


class SiteConfigRepository(BaseRepository[SiteConfig]):
    """Data access for site settings."""

    model = SiteConfig

    def create(self, *, key, value):
        return self.model.objects.create(key=key, value=value)
