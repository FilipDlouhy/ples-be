from apps.user.repositories import token_repository, user_repository

from .auth import AuthService

auth_service = AuthService(user_repository=user_repository, token_repository=token_repository)

__all__ = ["auth_service"]
