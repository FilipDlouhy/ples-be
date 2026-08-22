from apps.salons.repositories import (
    maker_repository,
    maker_reservation_repository,
    maker_time_repository,
    treatment_repository,
)

from .bookings import BookingService
from .emails import MakerEmailService
from .makers import MakerService

email_service = MakerEmailService()
maker_service = MakerService(
    maker_repository=maker_repository,
    treatment_repository=treatment_repository,
    maker_time_repository=maker_time_repository,
)
booking_service = BookingService(
    maker_repository=maker_repository,
    maker_time_repository=maker_time_repository,
    maker_reservation_repository=maker_reservation_repository,
    email_service=email_service,
)

__all__ = ["booking_service", "email_service", "maker_service"]
