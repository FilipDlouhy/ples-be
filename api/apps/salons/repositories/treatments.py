from apps.salons.models import Treatment
from common.repositories import BaseRepository


class TreatmentRepository(BaseRepository[Treatment]):
    """Data access for the services makers offer."""

    model = Treatment

    def create(self, *, maker, service):
        return self.model.objects.create(maker=maker, service=service)
