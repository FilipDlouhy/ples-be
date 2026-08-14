from apps.content.models import TicketContent
from common.repositories import BaseRepository


class TicketContentRepository(BaseRepository[TicketContent]):
    """Data access for the ticket presale settings of the landing page."""

    model = TicketContent

    def get_first(self) -> TicketContent | None:
        return self.model.objects.select_related("contact").order_by("id").first()

    def create(self, *, reservation_from, contact):
        return self.model.objects.create(reservation_from=reservation_from, contact=contact)
