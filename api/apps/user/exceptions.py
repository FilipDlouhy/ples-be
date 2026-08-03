from rest_framework import status

from common.exceptions import ApplicationError


class BadCredentialsError(ApplicationError):
    """Wrong email or password, or the account is not staff."""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__("Bad credentials.")

    def to_data(self):
        return {"message": self.message}
