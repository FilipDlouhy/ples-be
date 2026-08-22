from django.db import models


class Maker(models.Model):
    """Hairdresser or make-up artist who works in the salon on the day of the ball."""

    name = models.CharField("jméno", max_length=255)
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "kadeřnice / kosmetička"
        verbose_name_plural = "kadeřnice / kosmetičky"

    def __str__(self):
        return self.name


class Treatment(models.Model):
    """Service a maker offers, for example hairstyle or make-up (the table maker_services of the Laravel app)."""

    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, related_name="treatments", verbose_name="kadeřnice / kosmetička")
    service = models.CharField("služba", max_length=255)
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "služba"
        verbose_name_plural = "služby"

    def __str__(self):
        return f"{self.maker} - {self.service}"


class MakerTime(models.Model):
    """Time slot in which a maker is not free. A booking creates one, the admin can add more."""

    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, related_name="blocked_times", verbose_name="kadeřnice / kosmetička")
    time = models.CharField("čas", max_length=4, help_text="Například 1430 pro 14:30.")
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["time", "maker_id"]
        verbose_name = "obsazený čas"
        verbose_name_plural = "obsazené časy"
        constraints = [
            models.UniqueConstraint(fields=["maker", "time"], name="salons_maker_time_unique_maker_time"),
        ]

    def __str__(self):
        return f"{self.time} {self.maker}"


class MakerReservation(models.Model):
    """Reservation of a maker made through the public form."""

    maker = models.ForeignKey(Maker, on_delete=models.PROTECT, related_name="reservations", verbose_name="kadeřnice / kosmetička")
    time = models.CharField("čas", max_length=4, help_text="Například 1430 pro 14:30.")
    service = models.CharField("služba", max_length=255)
    name = models.CharField("jméno", max_length=255)
    phone = models.CharField("telefon", max_length=255)
    email = models.CharField("e-mail", max_length=255)
    consent = models.BooleanField("souhlas se zpracováním osobních údajů")
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "rezervace salonu"
        verbose_name_plural = "rezervace salonu"

    def __str__(self):
        return f"{self.time} {self.name}"
