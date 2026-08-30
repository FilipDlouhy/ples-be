import json
from dataclasses import dataclass
from datetime import UTC

from rest_framework import serializers

from common.formats import DATABASE_DATETIME_FORMAT, LARAVEL_DATETIME_FORMAT
from common.serializers import LaravelSerializer


@dataclass(frozen=True)
class SeatSpec:
    table: int
    letter: str
    kind: str


@dataclass(frozen=True)
class SeatMap:
    available_stands: int
    free_seats: int
    taken_seats: int
    seats: list


@dataclass(frozen=True)
class CreatedReservation:
    reservation: object
    seats: list


@dataclass(frozen=True)
class EventOverview:
    taken_seats: int
    free_seats: int
    free_dinner_seats: int
    free_plain_seats: int
    available_stands: int
    sold_stands: int
    money_raised: int


@dataclass(frozen=True)
class PreparedEvent:
    event: object
    seats_created: int


@dataclass(frozen=True)
class SeedResult:
    events_created: int
    seats_created: int
    makers_created: int
    services_created: int
    contacts_created: int
    config_created: int


class SeatIdsField(serializers.ListField):
    """List of seat ids; the 2023 frontend sent it as a JSON string like "[101,102]"."""

    child = serializers.IntegerField(min_value=1)

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError:
                self.fail("not_a_list", input_type="str")
        return super().to_internal_value(data)


class ReservationRequestSerializer(LaravelSerializer):
    # the 2023 frontend sent stand as a string, IntegerField accepts both
    stand = serializers.IntegerField(min_value=0, required=False, allow_null=True, default=0)
    seats = SeatIdsField(required=False, allow_null=True, default=list)
    note = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")


class SeatResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    alias = serializers.CharField()
    typ = serializers.CharField(source="kind")
    rezervace = serializers.IntegerField(source="reservation_id", allow_null=True)
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class SeatMapResponseSerializer(serializers.Serializer):
    availableStands = serializers.IntegerField(source="available_stands")
    freeSeats = serializers.IntegerField(source="free_seats")
    takenSeats = serializers.IntegerField(source="taken_seats")
    seats = SeatResponseSerializer(many=True)


class ReservationCreatedSerializer(serializers.Serializer):
    """The reservation as Laravel returned it right after the insert: numbers are numbers."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    tel = serializers.CharField(allow_blank=True)
    note = serializers.CharField(allow_blank=True)
    stand = serializers.IntegerField()
    price_all = serializers.IntegerField()
    status = serializers.IntegerField()
    consent = serializers.IntegerField()
    date_payment = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC, allow_null=True)
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class ReservationCreatedResponseSerializer(serializers.Serializer):
    reservation = ReservationCreatedSerializer()
    seats = SeatResponseSerializer(many=True)


class ReservationSearchResponseSerializer(serializers.Serializer):
    """The reservation as Laravel read it from MySQL: stand and price_all are strings (varchar columns)."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()
    tel = serializers.CharField(allow_blank=True)
    note = serializers.CharField(allow_blank=True)
    stand = serializers.CharField()
    price_all = serializers.CharField()
    status = serializers.IntegerField()
    date_payment = serializers.DateTimeField(format=DATABASE_DATETIME_FORMAT, default_timezone=UTC, allow_null=True)
    consent = serializers.IntegerField()
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
