from apps.reservations.dtos import SeatMap
from common.exceptions import NotFoundError


class SeatMapService:
    """Public seat map with the counters of the active event."""

    def __init__(self, *, event_repository, seat_repository, reservation_repository):
        self.event_repository = event_repository
        self.seat_repository = seat_repository
        self.reservation_repository = reservation_repository

    def get_map(self):
        event = self.event_repository.get_active()
        if event is None:
            raise NotFoundError("There is no active event.")
        seats = self.seat_repository.list_for_event(event=event)
        free_seats = 0
        for seat in seats:
            if seat.reservation_id is None:
                free_seats += 1
        taken_stands = self.reservation_repository.total_stands(event=event)
        return SeatMap(
            available_stands=event.stand_capacity - taken_stands,
            free_seats=free_seats,
            taken_seats=len(seats) - free_seats,
            seats=seats,
        )
