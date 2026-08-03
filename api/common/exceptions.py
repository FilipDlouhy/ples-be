from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ApplicationError(Exception):
    """Base of the errors raised by services; the handler turns it into a response with status_code."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def to_data(self):
        return {"detail": self.message}


class BadRequestError(ApplicationError):
    """Wrong request, answered with the Laravel shape {"error": "..."}."""

    def to_data(self):
        return {"error": self.message}


class NotFoundError(ApplicationError):
    """Resource not found."""

    status_code = status.HTTP_404_NOT_FOUND


class ConflictError(ApplicationError):
    """Resource already exists."""

    status_code = status.HTTP_409_CONFLICT


def collect_messages(detail):
    """Flatten DRF error details into a list of texts."""
    messages = []
    if isinstance(detail, dict):
        for value in detail.values():
            messages.extend(collect_messages(value))
    elif isinstance(detail, list):
        for value in detail:
            messages.extend(collect_messages(value))
    else:
        messages.append(str(detail))
    return messages


def laravel_validation_data(detail):
    """Build the Laravel validation error: {"message": "...", "errors": {"field": ["..."]}}."""
    errors = {}
    all_messages = []
    for field, value in detail.items():
        messages = collect_messages(value)
        errors[field] = messages
        all_messages.extend(messages)
    message = all_messages[0]
    if len(all_messages) == 2:
        message = f"{message} (and 1 more error)"
    elif len(all_messages) > 2:
        message = f"{message} (and {len(all_messages) - 1} more errors)"
    return {"message": message, "errors": errors}


def custom_exception_handler(exc, context):
    """Answer errors in the shapes the Laravel API used."""
    if isinstance(exc, ApplicationError):
        return Response(exc.to_data(), status=exc.status_code)
    if isinstance(exc, ValidationError):
        return Response(laravel_validation_data(exc.detail), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({"message": "Unauthenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    if isinstance(exc, PermissionDenied):
        return Response({"message": "This action is unauthorized."}, status=status.HTTP_403_FORBIDDEN)
    return exception_handler(exc, context)
