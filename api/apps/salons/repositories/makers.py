from apps.salons.models import Maker
from common.repositories import BaseRepository


class MakerRepository(BaseRepository[Maker]):
    """Data access for makers."""

    model = Maker

    def create(self, *, name):
        return self.model.objects.create(name=name)
