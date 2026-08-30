from .events import EventRepository
from .reservations import ReservationRepository
from .seats import SeatRepository

event_repository = EventRepository()
reservation_repository = ReservationRepository()
seat_repository = SeatRepository()

__all__ = ["event_repository", "reservation_repository", "seat_repository"]
