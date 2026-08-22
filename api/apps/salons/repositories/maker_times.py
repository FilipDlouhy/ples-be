from apps.salons.models import MakerTime
from common.repositories import BaseRepository


class MakerTimeRepository(BaseRepository[MakerTime]):
    """Data access for the times in which a maker is not free."""

    model = MakerTime

    def create(self, *, maker, time):
        return self.model.objects.create(maker=maker, time=time)

    def delete_for_slot(self, *, maker_id, time) -> None:
        self.model.objects.filter(maker_id=maker_id, time=time).delete()
