from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AccountAdmin(UserAdmin):
    """Staff accounts; only is_staff users can log in to the API."""

    list_display = ["username", "email", "first_name", "last_name", "is_staff"]
