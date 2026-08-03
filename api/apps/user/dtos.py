from dataclasses import dataclass

from rest_framework import serializers

from common.serializers import LaravelSerializer

from .models import User


@dataclass(frozen=True)
class AuthSession:
    user: User
    token: str


class LoginRequestSerializer(LaravelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source="username")
    email = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = UserResponseSerializer()
    token = serializers.CharField()
