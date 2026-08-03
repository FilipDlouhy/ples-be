from django.db.models import Model


class BaseRepository[T: Model]:
    """Queries shared by all repositories."""

    model: type[T]

    def get_by_id(self, pk) -> T | None:
        return self.model.objects.filter(pk=pk).first()

    def get_by_id_for_update(self, pk) -> T | None:
        return self.model.objects.select_for_update().filter(pk=pk).first()

    def get_all(self) -> list[T]:
        return list(self.model.objects.all())

    def count(self) -> int:
        return self.model.objects.count()

    def delete(self, instance: T) -> None:
        instance.delete()

    def bulk_create(self, instances: list[T]) -> None:
        self.model.objects.bulk_create(instances)
