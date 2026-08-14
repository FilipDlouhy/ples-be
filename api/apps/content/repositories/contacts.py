from apps.content.models import Contact
from common.repositories import BaseRepository


class ContactRepository(BaseRepository[Contact]):
    """Data access for the contacts of the landing page."""

    model = Contact

    def list_excluding_role(self, role) -> list[Contact]:
        return list(self.model.objects.exclude(role=role).order_by("id"))

    def create(self, *, role, name, email, phone):
        return self.model.objects.create(role=role, name=name, email=email, phone=phone)
