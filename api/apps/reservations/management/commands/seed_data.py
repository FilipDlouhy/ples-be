from django.core.management.base import BaseCommand

from apps.reservations.services import seed_service


class Command(BaseCommand):
    help = (
        "Load the event with seats, the salon makers, the landing page contacts and the site settings "
        "when their tables are empty. Safe to run repeatedly."
    )

    def handle(self, *args, **options):
        seeded = seed_service.seed_reference_data()
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {seeded.events_created} event with {seeded.seats_created} seats, "
            f"{seeded.makers_created} makers with {seeded.services_created} services, "
            f"{seeded.contacts_created} landing page contacts and {seeded.config_created} settings."
        ))
