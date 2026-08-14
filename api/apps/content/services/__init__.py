from apps.content.repositories import contact_repository, content_repository, ticket_content_repository

from .content import ContentService

content_service = ContentService(
    content_repository=content_repository,
    contact_repository=contact_repository,
    ticket_content_repository=ticket_content_repository,
)

__all__ = ["content_service"]
