from django.db import transaction

from apps.salons.dtos import MakerOptions
from apps.salons.time_slots import TIME_SLOTS

# Taken from the legacy GET /api/makers of the 2024 ball
MAKER_NAMES = [
    "Barbora Jančí",
    "Veronika Pospíšilová",
    "Jana Vlčková",
    "Mirka Surmařová",
    "Vendula Rečková",
]
# (index in MAKER_NAMES, service), in the order of the legacy service ids 1-6
TREATMENTS = [
    (0, "Účes"),
    (1, "Účes"),
    (2, "Účes"),
    (3, "Make-up"),
    (4, "Make-up"),
    (2, "Make-up"),
]


class MakerService:
    """Makers with their services and the free times for the booking form."""

    def __init__(self, *, maker_repository, treatment_repository, maker_time_repository):
        self.maker_repository = maker_repository
        self.treatment_repository = treatment_repository
        self.maker_time_repository = maker_time_repository

    def get_options(self):
        """Get the makers, their services and, for every time slot, the makers that are not blocked in it."""
        makers = self.maker_repository.get_all()
        blocked = set()
        for maker_time in self.maker_time_repository.get_all():
            blocked.add((maker_time.maker_id, maker_time.time))

        available_times = {}
        for time_slot in TIME_SLOTS:
            free_maker_ids = []
            for maker in makers:
                if (maker.id, time_slot) not in blocked:
                    free_maker_ids.append(maker.id)
            available_times[time_slot] = free_maker_ids
        return MakerOptions(
            makers=makers,
            available_times=available_times,
            treatments=self.treatment_repository.get_all(),
        )

    @transaction.atomic
    def seed_makers(self):
        """Create the makers and their services when there is no maker, return (makers, services) created."""
        if self.maker_repository.count() > 0:
            return 0, 0
        makers = []
        for name in MAKER_NAMES:
            makers.append(self.maker_repository.create(name=name))
        for maker_index, service in TREATMENTS:
            self.treatment_repository.create(maker=makers[maker_index], service=service)
        return len(MAKER_NAMES), len(TREATMENTS)
