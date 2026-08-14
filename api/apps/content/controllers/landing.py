from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from apps.content.dtos import LandingPageResponseSerializer
from apps.content.services import content_service


class LandingController(ViewSet):
    """Public texts, contacts and ticket presale settings of the landing page."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public"

    def list(self, request):
        landing = content_service.get_landing()
        return Response(LandingPageResponseSerializer(landing).data)
