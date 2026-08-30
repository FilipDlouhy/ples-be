from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from apps.reservations.dtos import SeatMapResponseSerializer
from apps.reservations.services import seat_map_service


class SeatMapController(ViewSet):
    """Public live seat map of the active event."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public"

    def list(self, request):
        seat_map = seat_map_service.get_map()
        return Response(SeatMapResponseSerializer(seat_map).data)
