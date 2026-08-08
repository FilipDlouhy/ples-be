from django.db import transaction

# URL of the SMSticket shop, taken from the static config.json of the 2026 site
DEFAULT_CONFIG = [
    (
        "TICKET_URL",
        "https://www.smsticket.cz/vstupenky/65581-xxiv-reprezentacni-ples-univerzity-tomase-bati-ve-zline-kongresove-centrum-zlin",
    ),
]


class SiteConfigService:
    """Settings of the public site."""

    def __init__(self, *, site_config_repository):
        self.site_config_repository = site_config_repository

    def get_all(self):
        """Get all settings as one flat object, the key is the setting name."""
        config = {}
        for item in self.site_config_repository.get_all():
            config[item.key] = item.value
        return config

    @transaction.atomic
    def seed_config(self):
        """Create the default settings when the table is empty, return how many were created."""
        if self.site_config_repository.count() > 0:
            return 0
        for key, value in DEFAULT_CONFIG:
            self.site_config_repository.create(key=key, value=value)
        return len(DEFAULT_CONFIG)
