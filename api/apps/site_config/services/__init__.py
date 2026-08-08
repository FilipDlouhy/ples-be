from apps.site_config.repositories import site_config_repository

from .site_config import SiteConfigService

site_config_service = SiteConfigService(site_config_repository=site_config_repository)

__all__ = ["site_config_service"]
