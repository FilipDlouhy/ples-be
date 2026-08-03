from .tokens import TokenRepository
from .users import UserRepository

token_repository = TokenRepository()
user_repository = UserRepository()

__all__ = ["token_repository", "user_repository"]
