from django.conf import settings
from django.db import models
from django.db.models import Q


class Event(models.Model):
    """One edition of the ball with its seat layout, standing capacity and ticket prices."""

    name = models.CharField("název", max_length=255)
    year = models.PositiveSmallIntegerField("rok", unique=True)
    event_date = models.DateField("datum plesu", null=True, blank=True)
    stand_capacity = models.PositiveIntegerField("kapacita míst na stání", default=434)
    stand_price = models.PositiveIntegerField("cena místa na stání (Kč)", default=350)
    seat_price = models.PositiveIntegerField("cena sezení bez večeře (Kč)", default=500)
    dinner_seat_price = models.PositiveIntegerField("cena sezení s večeří (Kč)", default=750)
    complimentary_value = models.PositiveIntegerField(
        "hodnota volných lístků (Kč)",
        default=0,
        help_text="Odečte se od vybrané částky v přehledu.",
    )
    is_active = models.BooleanField("aktivní", default=False)

    class Meta:
        ordering = ["-year"]
        verbose_name = "ročník"
        verbose_name_plural = "ročníky"
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="reservations_event_single_active",
                violation_error_message="Aktivní může být jen jeden ročník. Nejdřív zrušte aktivitu u jiného ročníku.",
            ),
        ]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """Reservation made by staff at the sales desk: some standing places and some seats."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reservations", verbose_name="ročník")
    name = models.CharField("jméno", max_length=125)
    email = models.CharField("e-mail", max_length=125)
    tel = models.CharField("telefon", max_length=155, blank=True)
    note = models.TextField("poznámka", blank=True)
    stand = models.PositiveIntegerField("místa na stání", default=0)
    price_all = models.PositiveIntegerField("cena celkem (Kč)", default=0)
    status = models.IntegerField("stav", default=1)
    date_payment = models.DateTimeField("datum platby", null=True, blank=True)
    consent = models.BooleanField("souhlas", default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="vytvořil",
    )
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "rezervace"
        verbose_name_plural = "rezervace"

    def __str__(self):
        return f"Rezervace {self.pk}"


class Seat(models.Model):
    """One seat at a table; kind 'raut' is the seating with dinner."""

    class Kind(models.TextChoices):
        RAUT = "raut", "S večeří"
        NORMAL = "normal", "Bez večeře"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="seats", verbose_name="ročník")
    table = models.PositiveSmallIntegerField("stůl")
    letter = models.CharField("písmeno", max_length=1)
    alias = models.CharField("označení", max_length=10)
    kind = models.CharField("typ", max_length=10, choices=Kind.choices, default=Kind.NORMAL)
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seats",
        verbose_name="rezervace",
    )
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["event_id", "table", "letter"]
        verbose_name = "místo"
        verbose_name_plural = "místa"
        constraints = [
            models.UniqueConstraint(fields=["event", "alias"], name="reservations_seat_unique_alias_per_event"),
        ]

    def __str__(self):
        return self.alias
