from django.contrib import admin

from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    """Settings of the public site."""

    list_display = ["key", "value"]
    search_fields = ["key", "value"]
