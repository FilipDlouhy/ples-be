from django.utils import timezone

from apps.reservations.models import Seat
from common.repositories import BaseRepository


class SeatRepository(BaseRepository[Seat]):
    """Data access for seats."""

    model = Seat

    def list_for_event(self, *, event) -> list[Seat]:
        return list(self.model.objects.filter(event=event).order_by("id"))

    def list_for_reservation(self, *, reservation) -> list[Seat]:
        return list(self.model.objects.filter(reservation=reservation).order_by("id"))

    def list_by_ids_for_update(self, *, event, seat_ids) -> list[Seat]:
        # ordered by id so that two requests lock seats in the same order
        seats = self.model.objects.select_for_update().filter(event=event, id__in=seat_ids).order_by("id")
        return list(seats)

    def count_taken(self, *, event) -> int:
        return self.model.objects.filter(event=event, reservation__isnull=False).count()

    def count_free(self, *, event) -> int:
        return self.model.objects.filter(event=event, reservation__isnull=True).count()

    def count_free_by_kind(self, *, event, kind) -> int:
        return self.model.objects.filter(event=event, reservation__isnull=True, kind=kind).count()

    def assign_to_reservation(self, *, seat_ids, reservation) -> None:
        self.model.objects.filter(id__in=seat_ids).update(reservation=reservation, updated_at=timezone.now())

    def release_reservation(self, *, reservation) -> None:
        self.model.objects.filter(reservation=reservation).update(reservation=None, updated_at=timezone.now())

    def create_for_event(self, *, event, specs) -> int:
        seats = []
        for spec in specs:
            seats.append(
                Seat(
                    event=event,
                    table=spec.table,
                    letter=spec.letter,
                    alias=f"{spec.table}/{spec.letter}",
                    kind=spec.kind,
                )
            )
        self.bulk_create(seats)
        return len(seats)
