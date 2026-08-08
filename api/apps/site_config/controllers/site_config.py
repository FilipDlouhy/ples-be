from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from apps.site_config.services import site_config_service


class SiteConfigController(ViewSet):
    """Public settings of the site, for example the ticket shop URL."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "public"

    def list(self, request):
        return Response(site_config_service.get_all())
