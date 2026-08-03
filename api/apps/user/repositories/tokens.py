from rest_framework.authtoken.models import Token

from common.repositories import BaseRepository


class TokenRepository(BaseRepository[Token]):
    """Data access for API tokens."""

    model = Token

    def get_or_create_for_user(self, user) -> Token:
        token, _ = self.model.objects.get_or_create(user=user)
        return token

    def delete_for_user(self, user) -> None:
        self.model.objects.filter(user=user).delete()
