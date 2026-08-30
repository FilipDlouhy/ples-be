from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.reservations.dtos import (
    ReservationCreatedResponseSerializer,
    ReservationRequestSerializer,
    ReservationSearchResponseSerializer,
)
from apps.reservations.services import reservation_service
from apps.user.authentication import BearerTokenAuthentication


class ReservationController(ViewSet):
    """Staff API to reserve standing places and seats and to search reservations, called with a Bearer token."""

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request):
        serializer = ReservationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        created = reservation_service.create(
            created_by=request.user,
            stand=data["stand"],
            seat_ids=data["seats"],
            note=data["note"],
        )
        return Response(ReservationCreatedResponseSerializer(created).data)

    @action(detail=False, methods=["get"], url_path=r"search/(?P<name>[^/]+)")
    def search(self, request, name):
        reservations = reservation_service.search(name=name)
        return Response(ReservationSearchResponseSerializer(reservations, many=True).data)
