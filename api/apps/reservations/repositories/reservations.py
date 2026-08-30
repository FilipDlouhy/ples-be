from django.db.models import Sum
from django.db.models.functions import Coalesce

from apps.reservations.models import Reservation
from common.repositories import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    """Data access for reservations."""

    model = Reservation

    def total_stands(self, *, event) -> int:
        result = self.model.objects.filter(event=event).aggregate(total=Coalesce(Sum("stand"), 0))
        return result["total"]

    def total_price(self, *, event) -> int:
        result = self.model.objects.filter(event=event).aggregate(total=Coalesce(Sum("price_all"), 0))
        return result["total"]

    def search_by_name(self, *, event, name) -> list[Reservation]:
        return list(self.model.objects.filter(event=event, name__icontains=name).order_by("id"))

    def create(self, *, event, name, email, tel, note, stand, price_all, status, consent, date_payment, created_by):
        return self.model.objects.create(
            event=event,
            name=name,
            email=email,
            tel=tel,
            note=note,
            stand=stand,
            price_all=price_all,
            status=status,
            consent=consent,
            date_payment=date_payment,
            created_by=created_by,
        )
