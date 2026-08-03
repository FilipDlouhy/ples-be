from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """Reads "Authorization: Bearer <token>" like Laravel Sanctum."""

    keyword = "Bearer"
