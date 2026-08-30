import datetime

from django.db import transaction

from apps.reservations.dtos import EventOverview, PreparedEvent, SeatSpec
from apps.reservations.models import Seat
from common.exceptions import ConflictError

# Hall layout of the 2024-2026 balls: 132 tables, A and B at every table, C and D except the
# tables 116-127 which have only 2 seats. Tables 1-110 are seated with dinner ("raut").
TABLE_COUNT = 132
LAST_RAUT_TABLE = 110
FIRST_TWO_SEAT_TABLE = 116
LAST_TWO_SEAT_TABLE = 127

FIRST_EVENT_YEAR = 2026
FIRST_EVENT_DATE = datetime.date(2026, 2, 20)
STAND_CAPACITY = 434

# Ticket prices of the 2026 ball (the Laravel code of the 2024 ball had 350, 500 and 750)
STAND_PRICE = 400
SEAT_PRICE = 650
DINNER_SEAT_PRICE = 990


class EventService:
    """Ball editions: dashboard overview, preparing the next year and the first edition seed."""

    def __init__(self, *, event_repository, seat_repository, reservation_repository):
        self.event_repository = event_repository
        self.seat_repository = seat_repository
        self.reservation_repository = reservation_repository

    def get_overview(self, *, event):
        """Counters of the old Laravel admin dashboard: seats, standing places and the money raised."""
        sold_stands = self.reservation_repository.total_stands(event=event)
        money_raised = self.reservation_repository.total_price(event=event) - event.complimentary_value
        return EventOverview(
            taken_seats=self.seat_repository.count_taken(event=event),
            free_seats=self.seat_repository.count_free(event=event),
            free_dinner_seats=self.seat_repository.count_free_by_kind(event=event, kind=Seat.Kind.RAUT),
            free_plain_seats=self.seat_repository.count_free_by_kind(event=event, kind=Seat.Kind.NORMAL),
            available_stands=event.stand_capacity - sold_stands,
            sold_stands=sold_stands,
            money_raised=money_raised,
        )

    @transaction.atomic
    def prepare_next_event(self, *, event):
        """Create an inactive edition for the next year with the same seat layout and prices, all seats free."""
        next_year = event.year + 1
        if self.event_repository.exists_with_year(next_year):
            raise ConflictError(f"Event for year {next_year} already exists.")
        new_event = self.event_repository.create(
            name=f"Reprezentační ples UTB {next_year}",
            year=next_year,
            event_date=None,
            stand_capacity=event.stand_capacity,
            stand_price=event.stand_price,
            seat_price=event.seat_price,
            dinner_seat_price=event.dinner_seat_price,
            complimentary_value=0,
            is_active=False,
        )
        specs = []
        for seat in self.seat_repository.list_for_event(event=event):
            specs.append(SeatSpec(table=seat.table, letter=seat.letter, kind=seat.kind))
        seats_created = self.seat_repository.create_for_event(event=new_event, specs=specs)
        return PreparedEvent(event=new_event, seats_created=seats_created)

    @transaction.atomic
    def seed_first_event(self):
        """Create the active 2026 edition with the hall layout when no edition exists, return (events, seats) created."""
        if self.event_repository.count() > 0:
            return 0, 0
        event = self.event_repository.create(
            name=f"Reprezentační ples UTB {FIRST_EVENT_YEAR}",
            year=FIRST_EVENT_YEAR,
            event_date=FIRST_EVENT_DATE,
            stand_capacity=STAND_CAPACITY,
            stand_price=STAND_PRICE,
            seat_price=SEAT_PRICE,
            dinner_seat_price=DINNER_SEAT_PRICE,
            complimentary_value=0,
            is_active=True,
        )
        seats_created = self.seat_repository.create_for_event(event=event, specs=self._default_layout())
        return 1, seats_created

    def _default_layout(self):
        specs = []
        for table in range(1, TABLE_COUNT + 1):
            kind = Seat.Kind.NORMAL
            if table <= LAST_RAUT_TABLE:
                kind = Seat.Kind.RAUT
            letters = ["A", "B", "C", "D"]
            if FIRST_TWO_SEAT_TABLE <= table <= LAST_TWO_SEAT_TABLE:
                letters = ["A", "B"]
            for letter in letters:
                specs.append(SeatSpec(table=table, letter=letter, kind=kind))
        return specs
