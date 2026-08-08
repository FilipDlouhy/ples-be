from django.db import models


class SiteConfig(models.Model):
    """One setting of the public site, for example the ticket shop URL under the key TICKET_URL."""

    key = models.CharField("klíč", max_length=100, unique=True)
    value = models.CharField("hodnota", max_length=1000)

    class Meta:
        ordering = ["key"]
        verbose_name = "nastavení"
        verbose_name_plural = "nastavení"

    def __str__(self):
        return self.key
