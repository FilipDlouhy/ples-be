from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from apps.salons.dtos import BookingRequestSerializer, BookingResultResponseSerializer, MakerOptionsResponseSerializer
from apps.salons.services import booking_service, maker_service


class MakerController(ViewSet):
    """Public API of the salon booking: makers with free times and the booking itself."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public"

    def list(self, request):
        options = maker_service.get_options()
        return Response(MakerOptionsResponseSerializer(options).data)

    def create(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = booking_service.book(
            maker=data["maker"],
            time_slot=data["time"],
            service=data["service"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            consent=data["consent"],
        )
        return Response(BookingResultResponseSerializer(result).data)
