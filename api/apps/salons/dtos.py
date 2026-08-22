from dataclasses import dataclass
from datetime import UTC

from rest_framework import serializers

from common.formats import LARAVEL_DATETIME_FORMAT
from common.serializers import LaravelSerializer


@dataclass(frozen=True)
class MakerOptions:
    makers: list
    available_times: dict
    treatments: list


@dataclass(frozen=True)
class BookingResult:
    reservation: object
    reserved_time: object


class BookingRequestSerializer(LaravelSerializer):
    # the frontend sends every value as a string, for example "maker": "1" and "consent": "true";
    # like in Laravel only the presence is checked, the service decides what a wrong maker or time means
    maker = serializers.CharField()
    time = serializers.CharField()
    service = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    consent = serializers.BooleanField()


class MakerResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class TreatmentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    maker_id = serializers.IntegerField()
    service = serializers.CharField()
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class MakerOptionsResponseSerializer(serializers.Serializer):
    makers = MakerResponseSerializer(many=True)
    availableTimes = serializers.DictField(source="available_times", child=serializers.ListField(child=serializers.IntegerField()))
    makerServices = TreatmentResponseSerializer(many=True, source="treatments")


class MakerReservationResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    maker = serializers.IntegerField(source="maker_id")
    time = serializers.CharField()
    service = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    consent = serializers.IntegerField()
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class ReservedTimeResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    maker_id = serializers.IntegerField()
    time = serializers.CharField()
    created_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)
    updated_at = serializers.DateTimeField(format=LARAVEL_DATETIME_FORMAT, default_timezone=UTC)


class BookingResultResponseSerializer(serializers.Serializer):
    reservation = MakerReservationResponseSerializer()
    reservedTime = ReservedTimeResponseSerializer(source="reserved_time")
