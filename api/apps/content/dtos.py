from dataclasses import dataclass

from rest_framework import serializers


@dataclass(frozen=True)
class TicketsInfo:
    reservations_from: object
    contact: object


@dataclass(frozen=True)
class LandingPage:
    contents: list
    contacts: list
    tickets: TicketsInfo


class ContentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()


class ContactResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField(allow_blank=True)


class TicketsResponseSerializer(serializers.Serializer):
    reservations_from = serializers.DateField()
    contact = ContactResponseSerializer()


class LandingPageResponseSerializer(serializers.Serializer):
    contents = ContentResponseSerializer(many=True)
    contacts = ContactResponseSerializer(many=True)
    tickets = TicketsResponseSerializer()
