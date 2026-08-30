from rest_framework.routers import SimpleRouter

from .controllers.reservations import ReservationController
from .controllers.seat_map import SeatMapController

router = SimpleRouter(trailing_slash=False)
router.register("pages/reservations", SeatMapController, basename="seat-map")
router.register("reservations", ReservationController, basename="reservation")

urlpatterns = router.urls
