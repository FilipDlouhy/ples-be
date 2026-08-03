from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.viewsets import ViewSet

from apps.user.authentication import BearerTokenAuthentication
from apps.user.dtos import LoginRequestSerializer, LoginResponseSerializer
from apps.user.services import auth_service


class AuthController(ViewSet):
    """Login that returns a Bearer token, and logout that deletes it."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    @action(detail=False, methods=["post"], throttle_classes=[ScopedRateThrottle])
    def login(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        session = auth_service.login(email=data["email"], password=data["password"])
        body = {"user": session.user, "token": session.token}
        return Response(LoginResponseSerializer(body).data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["post"],
        authentication_classes=[BearerTokenAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        auth_service.logout(user=request.user)
        return Response({"message": "Logged out."})
