from .contacts import ContactRepository
from .contents import ContentRepository
from .tickets import TicketContentRepository

contact_repository = ContactRepository()
content_repository = ContentRepository()
ticket_content_repository = TicketContentRepository()

__all__ = ["contact_repository", "content_repository", "ticket_content_repository"]
