from apps.content.services import content_service
from apps.reservations.repositories import event_repository, reservation_repository, seat_repository
from apps.salons.services import maker_service
from apps.site_config.services import site_config_service

from .events import EventService
from .reservations import ReservationService
from .seat_map import SeatMapService
from .seed import SeedService

event_service = EventService(
    event_repository=event_repository,
    seat_repository=seat_repository,
    reservation_repository=reservation_repository,
)
seat_map_service = SeatMapService(
    event_repository=event_repository,
    seat_repository=seat_repository,
    reservation_repository=reservation_repository,
)
reservation_service = ReservationService(
    event_repository=event_repository,
    seat_repository=seat_repository,
    reservation_repository=reservation_repository,
)
seed_service = SeedService(
    event_service=event_service,
    maker_service=maker_service,
    content_service=content_service,
    site_config_service=site_config_service,
)

__all__ = ["event_service", "reservation_service", "seat_map_service", "seed_service"]
