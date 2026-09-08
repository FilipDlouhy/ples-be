from django.contrib import admin, messages

from apps.reservations.models import Event, Reservation, Seat
from apps.reservations.services import event_service, reservation_service
from common.exceptions import ApplicationError


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Ball editions with the dashboard overview; the action prepares the next year."""

    list_display = ["name", "year", "event_date", "is_active", "overview"]
    list_filter = ["is_active"]
    actions = ["prepare_next_event"]

    @admin.display(description="Přehled")
    def overview(self, obj):
        data = event_service.get_overview(event=obj)
        return (
            f"Místa: volných {data.free_seats} (s večeří {data.free_dinner_seats}, bez večeře {data.free_plain_seats}), "
            f"obsazených {data.taken_seats} | "
            f"Stání: volných {data.available_stands}, prodaných {data.sold_stands} | "
            f"Vybráno: {data.money_raised} Kč"
        )

    @admin.action(description="Připravit další ročník")
    def prepare_next_event(self, request, queryset):
        for event in queryset:
            try:
                prepared = event_service.prepare_next_event(event=event)
                self.message_user(
                    request,
                    f"{prepared.event.name}: vytvořeno {prepared.seats_created} volných míst, ročník není aktivní.",
                    level=messages.SUCCESS,
                )
            except ApplicationError as error:
                self.message_user(request, f"{event}: {error.message}", level=messages.WARNING)


class FreeSeatFilter(admin.SimpleListFilter):
    """Filter seats by whether a reservation holds them."""

    title = "obsazení"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return [("free", "Volná"), ("taken", "Obsazená")]

    def queryset(self, request, queryset):
        if self.value() == "free":
            return queryset.filter(reservation__isnull=True)
        if self.value() == "taken":
            return queryset.filter(reservation__isnull=False)
        return queryset


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    """Seats of all editions, read only."""

    list_display = ["alias", "event", "table", "letter", "kind", "state"]
    list_filter = ["event", "kind", FreeSeatFilter]
    list_select_related = ["event"]
    search_fields = ["alias"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Obsazení")
    def state(self, obj):
        if obj.reservation_id is None:
            return "Volné"
        return f"Rezervace {obj.reservation_id}"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservations made through the API; they can only be searched and cancelled."""

    list_display = ["id", "name", "email", "note", "stand", "price_all", "date_payment", "seat_list", "event"]
    list_filter = ["event"]
    list_select_related = ["event"]
    list_per_page = 10
    search_fields = ["name", "email", "note", "seats__alias"]
    fields = [
        "event",
        "name",
        "email",
        "tel",
        "note",
        "stand",
        "price_all",
        "status",
        "date_payment",
        "consent",
        "seat_list",
        "created_by",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["seat_list", "created_by", "created_at", "updated_at"]
    actions = ["cancel_reservations"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("seats")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def delete_model(self, request, obj):
        reservation_service.cancel(reservation_id=obj.pk)

    def delete_queryset(self, request, queryset):
        for reservation in queryset:
            reservation_service.cancel(reservation_id=reservation.pk)

    @admin.action(description="Zrušit rezervaci")
    def cancel_reservations(self, request, queryset):
        done = 0
        for reservation in queryset:
            try:
                reservation_service.cancel(reservation_id=reservation.pk)
                done += 1
            except ApplicationError as error:
                self.message_user(request, f"{reservation}: {error.message}", level=messages.WARNING)
        self.message_user(request, f"Zrušeno rezervací: {done}", level=messages.SUCCESS)

    @admin.display(description="Místa")
    def seat_list(self, obj):
        aliases = []
        for seat in obj.seats.all():
            aliases.append(seat.alias)
        return ", ".join(aliases)
