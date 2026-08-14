from django.contrib import admin

from .models import Contact, Content, TicketContent


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Texts of the landing page."""

    list_display = ["id", "title", "content"]
    search_fields = ["title", "content"]

    def get_readonly_fields(self, request, obj=None):
        # the landing page finds a text by its title, so only the text can be changed
        if obj is not None:
            return ["title"]
        return []


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Contacts of the landing page."""

    list_display = ["id", "role", "name", "email", "phone"]
    search_fields = ["role", "name", "email"]

    def get_readonly_fields(self, request, obj=None):
        # the role "tickets" marks the presale contact, so it is not changed here
        if obj is not None:
            return ["role"]
        return []


@admin.register(TicketContent)
class TicketContentAdmin(admin.ModelAdmin):
    """Start of the ticket sales and the contact for it."""

    list_display = ["id", "reservation_from", "contact"]
    list_select_related = ["contact"]
