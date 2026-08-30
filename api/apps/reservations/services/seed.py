from django.db import transaction

from apps.reservations.dtos import SeedResult


class SeedService:
    """Loads all reference data of the project (event with seats, makers, landing page, settings), no users and no reservations."""

    def __init__(self, *, event_service, maker_service, content_service, site_config_service):
        self.event_service = event_service
        self.maker_service = maker_service
        self.content_service = content_service
        self.site_config_service = site_config_service

    @transaction.atomic
    def seed_reference_data(self):
        events_created, seats_created = self.event_service.seed_first_event()
        makers_created, services_created = self.maker_service.seed_makers()
        return SeedResult(
            events_created=events_created,
            seats_created=seats_created,
            makers_created=makers_created,
            services_created=services_created,
            contacts_created=self.content_service.seed_landing(),
            config_created=self.site_config_service.seed_config(),
        )
