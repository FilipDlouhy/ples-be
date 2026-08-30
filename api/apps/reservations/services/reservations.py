from django.db import transaction
from django.utils import timezone

from apps.reservations.dtos import CreatedReservation
from apps.reservations.exceptions import NothingSelectedError, SeatsTakenError, StandsLimitError
from apps.reservations.models import Seat
from common.exceptions import BadRequestError, NotFoundError

# The Laravel API saved every staff reservation under this fixed contact
STAFF_NAME = "Admin"
STAFF_EMAIL = "ples@sutb.cz"


class ReservationService:
    """Creating, searching and cancelling staff reservations of standing places and seats."""

    def __init__(self, *, event_repository, seat_repository, reservation_repository):
        self.event_repository = event_repository
        self.seat_repository = seat_repository
        self.reservation_repository = reservation_repository

    @transaction.atomic
    def create(self, *, created_by, stand, seat_ids, note):
        # The event row is locked, so two requests for the same event run one after another
        event = self.event_repository.get_active_for_update()
        if event is None:
            raise BadRequestError("There is no active event.")

        # Laravel treated a missing or null value as 0 / empty
        if stand is None:
            stand = 0
        if seat_ids is None:
            seat_ids = []
        if note is None:
            note = ""

        unique_ids = []
        for seat_id in seat_ids:
            if seat_id not in unique_ids:
                unique_ids.append(seat_id)

        if stand == 0 and len(unique_ids) == 0:
            raise NothingSelectedError()

        available_stands = event.stand_capacity - self.reservation_repository.total_stands(event=event)
        if stand > available_stands:
            raise StandsLimitError(requested=stand, available=available_stands)

        seats = self.seat_repository.list_by_ids_for_update(event=event, seat_ids=unique_ids)
        if len(seats) != len(unique_ids):
            raise BadRequestError("Some seats do not exist!")
        taken_seats = []
        for seat in seats:
            if seat.reservation_id is not None:
                taken_seats.append(seat)
        if len(taken_seats) > 0:
            raise SeatsTakenError(seats=taken_seats)

        reservation = self.reservation_repository.create(
            event=event,
            name=STAFF_NAME,
            email=STAFF_EMAIL,
            tel="",
            note=note,
            stand=stand,
            price_all=self._total_price(event=event, stand=stand, seats=seats),
            status=1,
            consent=True,
            date_payment=timezone.now(),
            created_by=created_by,
        )
        self.seat_repository.assign_to_reservation(seat_ids=unique_ids, reservation=reservation)
        return CreatedReservation(
            reservation=reservation,
            seats=self.seat_repository.list_for_reservation(reservation=reservation),
        )

    def search(self, *, name):
        """Find the reservations of the active event whose name contains the text."""
        event = self.event_repository.get_active()
        if event is None:
            return []
        return self.reservation_repository.search_by_name(event=event, name=name)

    @transaction.atomic
    def cancel(self, *, reservation_id):
        """Delete the reservation, its seats and standing places become free."""
        reservation = self.reservation_repository.get_by_id_for_update(reservation_id)
        if reservation is None:
            raise NotFoundError("Reservation not found.")
        self.seat_repository.release_reservation(reservation=reservation)
        self.reservation_repository.delete(reservation)

    def _total_price(self, *, event, stand, seats):
        total = stand * event.stand_price
        for seat in seats:
            if seat.kind == Seat.Kind.RAUT:
                total += event.dinner_seat_price
            else:
                total += event.seat_price
        return total
