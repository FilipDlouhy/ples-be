from apps.user.models import User
from common.repositories import BaseRepository


class UserRepository(BaseRepository[User]):
    """Data access for user accounts."""

    model = User

    def get_by_email(self, email) -> User | None:
        return self.model.objects.filter(email__iexact=email).order_by("id").first()
