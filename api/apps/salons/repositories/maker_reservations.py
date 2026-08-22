from apps.salons.models import MakerReservation
from common.repositories import BaseRepository


class MakerReservationRepository(BaseRepository[MakerReservation]):
    """Data access for the reservations of makers."""

    model = MakerReservation

    def create(self, *, maker, time, service, name, phone, email, consent):
        return self.model.objects.create(
            maker=maker,
            time=time,
            service=service,
            name=name,
            phone=phone,
            email=email,
            consent=consent,
        )
