from apps.reservations.models import Event
from common.repositories import BaseRepository


class EventRepository(BaseRepository[Event]):
    """Data access for ball editions."""

    model = Event

    def get_active(self) -> Event | None:
        return self.model.objects.filter(is_active=True).first()

    def get_active_for_update(self) -> Event | None:
        return self.model.objects.select_for_update().filter(is_active=True).first()

    def exists_with_year(self, year) -> bool:
        return self.model.objects.filter(year=year).exists()

    def create(
        self,
        *,
        name,
        year,
        event_date,
        stand_capacity,
        stand_price,
        seat_price,
        dinner_seat_price,
        complimentary_value,
        is_active,
    ):
        return self.model.objects.create(
            name=name,
            year=year,
            event_date=event_date,
            stand_capacity=stand_capacity,
            stand_price=stand_price,
            seat_price=seat_price,
            dinner_seat_price=dinner_seat_price,
            complimentary_value=complimentary_value,
            is_active=is_active,
        )
