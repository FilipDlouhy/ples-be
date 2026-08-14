from django.db import models


class Content(models.Model):
    """One text block of the landing page, identified by its title."""

    title = models.CharField("název sekce", max_length=25)
    content = models.TextField("text")
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "text úvodní stránky"
        verbose_name_plural = "texty úvodní stránky"

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Contact person of the landing page; the contact with the role "tickets" belongs to the ticket presale."""

    role = models.CharField("role", max_length=255)
    name = models.CharField("jméno", max_length=255)
    email = models.CharField("e-mail", max_length=255)
    phone = models.CharField("telefon", max_length=255, blank=True)
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "kontakt"
        verbose_name_plural = "kontakty"

    def __str__(self):
        return f"{self.role}: {self.name}"


class TicketContent(models.Model):
    """Ticket presale settings: the date when the reservations start and the contact for questions (the table tickets)."""

    reservation_from = models.DateField("prodej lístků od")
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="+", verbose_name="kontakt")
    created_at = models.DateTimeField("vytvořeno", auto_now_add=True)
    updated_at = models.DateTimeField("upraveno", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "prodej lístků"
        verbose_name_plural = "prodej lístků"

    def __str__(self):
        return f"Prodej lístků od {self.reservation_from}"
