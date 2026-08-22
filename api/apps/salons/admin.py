from django.contrib import admin

from apps.salons.services import booking_service
from apps.salons.time_slots import format_time

from .models import Maker, MakerReservation, MakerTime, Treatment


@admin.register(Maker)
class MakerAdmin(admin.ModelAdmin):
    """Hairdressers and make-up artists."""

    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    """Services of the makers."""

    list_display = ["id", "maker", "service"]
    list_filter = ["maker"]
    list_select_related = ["maker"]


@admin.register(MakerTime)
class MakerTimeAdmin(admin.ModelAdmin):
    """Times in which a maker is not free; add one here to close a time for a maker."""

    list_display = ["id", "maker", "time_label"]
    list_filter = ["maker", "time"]
    list_select_related = ["maker"]

    @admin.display(description="Čas")
    def time_label(self, obj):
        return format_time(obj.time)


@admin.register(MakerReservation)
class MakerReservationAdmin(admin.ModelAdmin):
    """Bookings made through the public form; deleting one frees the time of the maker."""

    list_display = ["id", "maker", "time_label", "service", "name", "phone", "email"]
    list_filter = ["maker", "time"]
    list_select_related = ["maker"]
    search_fields = ["maker__name", "name", "phone", "email"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def delete_model(self, request, obj):
        booking_service.cancel(reservation=obj)

    def delete_queryset(self, request, queryset):
        for reservation in queryset:
            booking_service.cancel(reservation=reservation)

    @admin.display(description="Čas")
    def time_label(self, obj):
        return format_time(obj.time)
