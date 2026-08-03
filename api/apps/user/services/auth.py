from apps.user.dtos import AuthSession
from apps.user.exceptions import BadCredentialsError


class AuthService:
    """Staff login with an API token, and logout."""

    def __init__(self, *, user_repository, token_repository):
        self.user_repository = user_repository
        self.token_repository = token_repository

    def login(self, *, email, password):
        """Check email and password of a staff account and return its API token."""
        user = self.user_repository.get_by_email(email)
        if user is None or not user.is_active or not user.is_staff:
            raise BadCredentialsError()
        if not user.check_password(password):
            raise BadCredentialsError()
        token = self.token_repository.get_or_create_for_user(user)
        return AuthSession(user=user, token=token.key)

    def logout(self, *, user):
        self.token_repository.delete_for_user(user)
