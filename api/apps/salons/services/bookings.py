from django.db import IntegrityError, transaction

from apps.salons.dtos import BookingResult
from apps.salons.time_slots import TIME_SLOTS, format_time
from common.exceptions import BadRequestError

WRONG_MAKER_MESSAGE = "Omlouváme se, nastala chyba a rezervace se bohužel nezdařila, zvolte prosím jinou obsluhu."
WRONG_TIME_MESSAGE = "Omlouváme se, nastala chyba a rezervace se bohužel nezdařila, zvolte prosím jiný čas."
SLOT_TAKEN_MESSAGE = 'Rezervace u vizážistky "{maker}" na {time} je již bohužel vytvořena, prosím zvolte jiný čas.'


class BookingService:
    """Salon bookings: a booking blocks the time of the maker, cancelling it frees the time again."""

    def __init__(self, *, maker_repository, maker_time_repository, maker_reservation_repository, email_service):
        self.maker_repository = maker_repository
        self.maker_time_repository = maker_time_repository
        self.maker_reservation_repository = maker_reservation_repository
        self.email_service = email_service

    @transaction.atomic
    def book(self, *, maker, time_slot, service, name, phone, email, consent):
        # the frontend sends the maker as a string; like in PHP anything that is not a number is a wrong maker
        if not maker.isascii() or not maker.isdigit() or len(maker) > 9:
            raise BadRequestError(WRONG_MAKER_MESSAGE)
        maker_row = self.maker_repository.get_by_id(int(maker))
        if maker_row is None:
            raise BadRequestError(WRONG_MAKER_MESSAGE)
        if time_slot not in TIME_SLOTS:
            raise BadRequestError(WRONG_TIME_MESSAGE)

        # the unique constraint of (maker, time) decides when two people book the same slot at once
        try:
            with transaction.atomic():
                reserved_time = self.maker_time_repository.create(maker=maker_row, time=time_slot)
        except IntegrityError:
            raise BadRequestError(SLOT_TAKEN_MESSAGE.format(maker=maker_row.name, time=format_time(time_slot)))

        reservation = self.maker_reservation_repository.create(
            maker=maker_row,
            time=time_slot,
            service=service,
            name=name,
            phone=phone,
            email=email,
            consent=consent,
        )
        self.email_service.send_confirmation(reservation=reservation)
        return BookingResult(reservation=reservation, reserved_time=reserved_time)

    @transaction.atomic
    def cancel(self, *, reservation):
        """Delete the booking and free the time of the maker."""
        self.maker_time_repository.delete_for_slot(maker_id=reservation.maker_id, time=reservation.time)
        self.maker_reservation_repository.delete(reservation)
