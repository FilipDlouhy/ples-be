from .maker_reservations import MakerReservationRepository
from .maker_times import MakerTimeRepository
from .makers import MakerRepository
from .treatments import TreatmentRepository

maker_repository = MakerRepository()
maker_reservation_repository = MakerReservationRepository()
maker_time_repository = MakerTimeRepository()
treatment_repository = TreatmentRepository()

__all__ = ["maker_repository", "maker_reservation_repository", "maker_time_repository", "treatment_repository"]
